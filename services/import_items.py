import pandas as pd

from services.db_session import SessionLocal
from models.category import Category
from models.item import Item

db = SessionLocal()

excel_file = "data/inventory_items.xlsx"

drug_category = db.query(Category).filter_by(name="دارو").first()
medical_category = db.query(Category).filter_by(name="تجهیزات پزشکی").first()

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

    drug_name = str(row[0]).strip()
    drug_form = str(row[1]).strip()

    if drug_name == "nan":
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

    item_name = str(row[0]).strip()

    if item_name == "nan":
        continue

    exists = (
        db.query(Item)
        .filter_by(item_name=item_name)
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