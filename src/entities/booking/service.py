from decimal import ROUND_HALF_UP, Decimal
from pathlib import Path
from typing import Tuple

from fpdf import FPDF

from src.core import config
from src.core.database.dependencies import UoWDI
from src.entities.booking.dto import BookingCreateDTO
from src.entities.booking.exceptions.domain import BookingsNotFoundError
from src.entities.booking.schemas import BookingCreateSchema, BookingReadSchema


class BookingService:
    def __init__(
        self,
        uow: UoWDI,
    ) -> None:
        self._uow = uow

    async def create_booking(
        self,
        booking_create_schema: BookingCreateSchema,
    ) -> BookingReadSchema:
        service = await self._uow.services.get_service_by_id(
            booking_create_schema.service_id,
        )

        commission_percent = Decimal(str(config.api.commission_percent))
        price = Decimal(service.price)
        commission_amount = (price * commission_percent / Decimal("100")).quantize(
            Decimal("0.01"),
            rounding=ROUND_HALF_UP,
        )
        total_amount = (price + commission_amount).quantize(
            Decimal("0.01"),
            rounding=ROUND_HALF_UP,
        )

        booking_create_dto = BookingCreateDTO(
            service_id=booking_create_schema.service_id,
            notary_profile_id=booking_create_schema.notary_profile_id,
            customer_profile_id=booking_create_schema.customer_profile_id,
            commission_percent=commission_percent,
            commission_amount=commission_amount,
            total_amount=total_amount,
        )

        booking_schema = await self._uow.booking_repository.create_booking(
            booking_create_dto,
        )
        return booking_schema

    async def generate_receipt_for_customer(
        self,
        booking_id: int,
        customer_profile_id: int,
    ) -> Tuple[bytes, str]:
        booking = await self._uow.booking_repository.get_booking_for_customer(
            booking_id,
            customer_profile_id,
        )
        if not booking:
            raise BookingsNotFoundError

        pdf_bytes = self._build_receipt_pdf(booking)
        filename = f"booking_{booking.id}_receipt.pdf"
        return pdf_bytes, filename

    async def get_bookings_by_id(
        self,
        id: int,
    ) -> list[BookingReadSchema]:
        booking_schemas = await self._uow.booking_repository.get_bookings_by_id(id)
        if not booking_schemas:
            raise BookingsNotFoundError
        return booking_schemas

    async def get_booking_by_customer_profile_id(
        self,
        customer_profile_id: int,
    ) -> list[BookingReadSchema]:
        booking_schemas = (
            await self._uow.booking_repository.get_bookings_by_customer_profile_id(
                customer_profile_id
            )
        )
        if not booking_schemas:
            raise BookingsNotFoundError
        return booking_schemas

    async def get_booking_by_notary_profile_id(
        self,
        notary_profile_id: int,
    ) -> list[BookingReadSchema]:
        booking_schemas = (
            await self._uow.booking_repository.get_bookings_by_notary_profile_id(
                notary_profile_id
            )
        )
        if not booking_schemas:
            raise BookingsNotFoundError
        return booking_schemas

    def _build_receipt_pdf(self, booking: BookingReadSchema) -> bytes:
        # 80mm receipt-style page
        pdf = FPDF(format=(80, 200))
        pdf.set_margins(4, 4, 4)
        pdf.add_page()
        pdf.set_auto_page_break(auto=True, margin=4)
        content_width = pdf.w - pdf.l_margin - pdf.r_margin
        left_col_width = content_width * 0.6

        font_family = self._ensure_pdf_fonts(pdf)

        pdf.set_font(font_family, "B", 12)
        pdf.cell(0, 6, "BOOKING RECEIPT", ln=1, align="C")
        pdf.set_font(font_family, "", 9)
        pdf.cell(0, 5, f"Booking ID: {booking.id}", ln=1, align="C")
        pdf.ln(2)

        pdf.cell(0, 0, "-" * 32, ln=1)
        pdf.ln(2)

        pdf.set_font(font_family, "B", 9)
        pdf.cell(0, 5, "SERVICE", ln=1)
        pdf.set_font(font_family, "", 9)
        pdf.set_x(pdf.l_margin)
        pdf.multi_cell(content_width, 4, booking.service.title)
        pdf.set_x(pdf.l_margin)
        pdf.multi_cell(content_width, 4, booking.service.description)
        pdf.ln(1)

        pdf.set_font(font_family, "B", 9)
        pdf.cell(0, 5, "NOTARY", ln=1)
        pdf.set_font(font_family, "", 9)
        pdf.set_x(pdf.l_margin)
        pdf.multi_cell(
            content_width,
            4,
            f"{booking.notary_profile.first_name} {booking.notary_profile.last_name}",
        )
        pdf.set_x(pdf.l_margin)
        pdf.multi_cell(content_width, 4, f"License: {booking.notary_profile.license_number}")
        pdf.set_x(pdf.l_margin)
        pdf.multi_cell(content_width, 4, f"INN: {booking.notary_profile.inn}")
        pdf.ln(1)

        pdf.cell(0, 0, "-" * 32, ln=1)
        pdf.ln(2)

        pdf.set_font(font_family, "B", 9)
        pdf.set_x(pdf.l_margin)
        pdf.cell(left_col_width, 5, "Item", border=0)
        pdf.cell(0, 5, "Amount", align="R", ln=1)
        pdf.set_font(font_family, "", 9)
        pdf.set_x(pdf.l_margin)
        pdf.cell(left_col_width, 5, "Service price", border=0)
        pdf.cell(0, 5, self._format_currency(booking.service.price), align="R", ln=1)
        pdf.set_x(pdf.l_margin)
        pdf.cell(
            left_col_width,
            5,
            f"Commission ({booking.commission_percent}%)",
            border=0,
        )
        pdf.cell(
            0,
            5,
            self._format_currency(booking.commission_amount),
            align="R",
            ln=1,
        )
        pdf.set_x(pdf.l_margin)
        pdf.cell(left_col_width, 5, "-" * 16, border=0)
        pdf.cell(0, 5, "-" * 10, align="R", ln=1)
        pdf.set_font(font_family, "B", 10)
        pdf.set_x(pdf.l_margin)
        pdf.cell(left_col_width, 6, "TOTAL", border=0)
        pdf.cell(0, 6, self._format_currency(booking.total_amount), align="R", ln=1)

        pdf.ln(2)
        pdf.cell(0, 0, "-" * 32, ln=1)
        pdf.ln(2)
        pdf.set_font(font_family, "", 9)
        pdf.set_x(pdf.l_margin)
        pdf.multi_cell(
            content_width,
            4,
            f"Customer: {booking.customer_profile.first_name} "
            f"{booking.customer_profile.last_name}",
        )

        output = pdf.output(dest="S")
        if isinstance(output, str):
            return output.encode("latin1")
        return bytes(output)

    def _format_currency(self, amount: Decimal) -> str:
        return f"{Decimal(str(amount)):.2f}"

    def _ensure_pdf_fonts(self, pdf: FPDF) -> str:
        """Register bundled Unicode font if it's not added yet."""
        font_family = "CourierPrime"
        font_path = Path(__file__).parent / "fonts" / "CourierPrime-Regular.ttf"
        font_path_str = str(font_path.resolve())

        # FPDF stores font keys in lowercase family + style suffix
        regular_key = (font_family.lower(), "")
        bold_key = (font_family.lower(), "B")

        if regular_key not in pdf.fonts:
            pdf.add_font(
                font_family,
                "",
                font_path_str,
                uni=True,
            )
        if bold_key not in pdf.fonts:
            # Bold variant not provided; reuse regular file to avoid errors on set_font(..., "B", ...)
            pdf.add_font(
                font_family,
                "B",
                font_path_str,
                uni=True,
            )

        pdf.set_font(font_family, "", 9)
        return font_family
