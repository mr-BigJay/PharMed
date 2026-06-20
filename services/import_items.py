import pandas as pd

from db import init_db
from services.db_session import SessionLocal
from models.category import Category
from models.item import Item


def main():
    init_db()
    db = SessionLocal()

    try:
        excel_file = "data/inventory_items.xlsx"

        drug_category = db.query(Category).filter_by(name="دارو").first()
        medical_category = (
            db.query(Category)
            .filter_by(name="تجهیزات پزشکی")
            .first()
        )

        if not drug_category or not medical_category:
            raise SystemExit(
                "Categories are missing. Run services/seed_categories.py first."
            )

        # ------------------
        # داروها
        # ------------------

        drugs_df = pd.read_excel(
            excel_file,
            sheet_name="دارو ها",
            header=None
        )

        drug_added = 0

        for _, row in drugs_df.iloc[1:].iterrows():

            if pd.isna(row[0]):
                continue

            drug_name = str(row[0]).strip()
            drug_form = "" if pd.isna(row[1]) else str(row[1]).strip()

            if not drug_name:
                continue

            exists = (
                db.query(Item)
                .filter_by(
                    item_name=drug_name,
                    item_form=drug_form
                )
                .first()
            )

            if exists:
                continue

            item = Item(
                category_id=drug_category.id,
                item_name=drug_name,
                item_form=drug_form,
                unit="عدد",
                minimum_stock=0
            )

            db.add(item)
            drug_added += 1

        # ------------------
        # تجهیزات پزشکی
        # ------------------

        medical_df = pd.read_excel(
            excel_file,
            sheet_name="تجهیزات پزشکی",
            header=None
        )

        medical_added = 0

        for _, row in medical_df.iloc[1:].iterrows():

            if pd.isna(row[0]):
                continue

            item_name = str(row[0]).strip()

            if not item_name:
                continue

            exists = (
                db.query(Item)
                .filter_by(
                    item_name=item_name,
                    category_id=medical_category.id
                )
                .first()
            )

            if exists:
                continue

            item = Item(
                category_id=medical_category.id,
                item_name=item_name,
                item_form="",
                unit="عدد",
                minimum_stock=0
            )

            db.add(item)
            medical_added += 1

        db.commit()

        print(f"Drugs Imported: {drug_added}")
        print(f"Medical Supplies Imported: {medical_added}")
        print(f"Total Imported: {drug_added + medical_added}")

    finally:
        db.close()


if __name__ == "__main__":
    main()