from typing import List
from pydantic import BaseModel
from docex import Pipeline, PDFLoader, LLMProcessor

from pydantic import BaseModel, Field
from datetime import date
from decimal import Decimal
from pydantic import BaseModel, Field
from typing import List, Optional


class MailingAddressDetails(BaseModel):
    addressee_name: str = Field(
        ..., description="Name of the person or entity the statement is mailed to."
    )
    address_lines: List[str] = Field(..., description="Lines of the mailing address.")


class AccountDetails(BaseModel):
    account_name: str = Field(
        ..., description="Official name associated with the bank account."
    )
    account_type: str = Field(
        ..., description="Type of bank account (e.g., Checking, Savings)."
    )
    account_number: str = Field(..., description="Bank account number.")


class StatementPeriod(BaseModel):
    description_text: str = Field(
        ..., description="The statement period as it appears on the document."
    )
    start_date: date = Field(..., description="Start date of the statement period.")
    end_date: date = Field(..., description="End date of the statement period.")


class BankHeader(BaseModel):
    document_title: str = Field(
        ..., description="Title of the bank statement document."
    )
    bank_name: str = Field(..., description="Name of the bank issuing the statement.")
    bank_address: Optional[str] = Field(None, description="Address of the bank.")
    mailing_address_details: MailingAddressDetails = Field(
        ..., description="Details of the mailing address on the statement."
    )
    account_details: AccountDetails = Field(
        ..., description="Details of the bank account."
    )
    statement_period: StatementPeriod = Field(
        ..., description="The period covered by the statement."
    )
    page_info: Optional[str] = Field(
        None, description="Pagination information (e.g., 'Page 1 of 1')."
    )


class DatedAmount(BaseModel):
    date_text: Optional[str] = Field(
        None, description="Date as text (e.g., '1 February')."
    )
    parsed_date: date = Field(..., description="Parsed date.")
    amount: Decimal = Field(..., description="Monetary amount.")


class AccountSummary(BaseModel):
    currency: str = Field(..., description="Currency code (e.g., GBP, USD).")
    balance_at_start_date: DatedAmount = Field(
        ..., description="Balance at the beginning of the statement period."
    )
    total_money_in: Decimal = Field(
        ...,
        description="Total amount of money credited to the account during the period.",
    )
    total_money_out: Decimal = Field(
        ...,
        description="Total amount of money debited from the account during the period.",
    )
    balance_at_end_date: DatedAmount = Field(
        ..., description="Balance at the end of the statement period."
    )


class Transaction(BaseModel):
    date_text: Optional[str] = Field(
        None,
        description="Original date string for the transaction from the statement, if available explicitly for this line.",
    )
    parsed_date: Optional[date] = Field(
        None, description="The fully parsed date of the transaction."
    )
    description: str = Field(
        ..., description="Description of the transaction, may include multiple lines."
    )
    money_out: Optional[Decimal] = Field(
        None, description="Amount debited for this transaction."
    )
    money_in: Optional[Decimal] = Field(
        None, description="Amount credited for this transaction."
    )
    balance: Decimal = Field(..., description="Account balance after this transaction.")


class BankStatement(BaseModel):
    bank_header: BankHeader
    account_summary: AccountSummary
    transactions: List[Transaction]


def main():
    # Set GEMINI_API_KEY environment variable or pass api_key
    processor = LLMProcessor(
        model="vertex_ai/gemini-2.5-pro-preview-05-06",
        temperature=0.1,
        max_tokens=32768,
        use_structured_output=True,
    )

    loader = PDFLoader(
        dpi=300,
        max_pages=20,
        thread_count=2,
    )

    pipeline = Pipeline(loader=loader, processor=processor)
    result = pipeline.process_document_sync(
        file_path="examples/bank_statement.pdf", schema=BankStatement
    )

    print(result)


if __name__ == "__main__":
    main()
