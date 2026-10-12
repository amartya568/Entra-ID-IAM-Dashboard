import csv
import os
from datetime import datetime


LOG_FILE = os.path.join(
    os.path.dirname(__file__),
    "iam_audit_log.csv"
)


def write_log(workflow, user_upn, action, result):

    file_exists = os.path.exists(LOG_FILE)

    with open(
        LOG_FILE,
        mode="a",
        newline="",
        encoding="utf-8"
    ) as file:

        writer = csv.writer(file)

        if not file_exists:
            writer.writerow([
                "Timestamp",
                "Workflow",
                "Employee",
                "Action",
                "Result"
            ])

        writer.writerow([
            datetime.now().isoformat(timespec="seconds"),
            workflow,
            user_upn,
            action,
            result
        ])


if __name__ == "__main__":

    write_log(
        "TEST",
        "test@example.com",
        "Test audit log",
        "Success"
    )

    print("Audit log entry created.")
    print(f"Log file: {LOG_FILE}")