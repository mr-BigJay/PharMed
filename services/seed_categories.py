from db import init_db
from services.bootstrap_service import bootstrap_reference_data


def main():
    init_db()
    stats = bootstrap_reference_data(
        verbose=True
    )
    print(
        f"Categories Seeded: {stats['categories']} added"
    )


if __name__ == "__main__":
    main()
