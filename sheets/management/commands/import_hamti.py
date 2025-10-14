import csv
from django.core.management.base import BaseCommand
from sheets.models import HamtiRecord


class Command(BaseCommand):
    help = "ایمپورت داده‌های بکاب همتی از CSV و ذخیره در مدل HamtiRecord"

    def add_arguments(self, parser):
        parser.add_argument("csv_file", type=str, help="نام فایل CSV شامل داده‌ها")

    def handle(self, *args, **options):
        csv_path = options["csv_file"]
        try:
            with open(csv_path, newline="", encoding="utf-8") as csvfile:
                # حذف فاصله از نام کلیدها با DictReader
                reader = csv.DictReader(csvfile)
                reader.fieldnames = [h.strip() for h in reader.fieldnames]  # حذف فاصله‌های اضافی
                count = 0

                for row in reader:
                    # حذف فاصله از کلیدهای هر ردیف
                    row = {k.strip(): (v.strip() if v else "") for k, v in row.items()}

                    code = row.get("کد سفارش", "")
                    if not code or "کد سفارش" in code:
                        continue

                    HamtiRecord.objects.update_or_create(
                        کد_سفارش=code,
                        defaults={
                            "تاریخ": row.get("تاریخ", ""),
                            "شهر": row.get("شهر", ""),
                            "منطقه": row.get("منطقه", ""),
                            "نوع_کسب_کار": row.get("نوع کسب کار", ""),
                            "حوزه_تخصصی": row.get("حوزه تخصصی", ""),
                            "نام_واحد_تجاری": row.get("نام واحد تجاری", ""),
                            "آدرس": row.get("آدرس", ""),
                            "شماره_مشتری": row.get("شماره مشتری", ""),
                            "نام_مدیریت": row.get("نام مدیریت", ""),
                            "مبدا_شماره": row.get("مبدا شماره", ""),
                            "مقصد": row.get("مقصد", ""),
                            "کارشناس_پیگیری": row.get("کارشناس پیگیری", ""),
                            "مبلغ_توافق_شده": row.get("مبلغ توافق شده", ""),
                            "مبلغ_فاکتور_شده": row.get("مبلغ فاکتور شده", ""),
                            "مبلغ_واریز_شده": row.get("مبلغ واریز شده", ""),
                            "قسط_اول": row.get("قسط اول", ""),
                            "قسط_دوم": row.get("قسط دوم", ""),
                            "نتیجه_تماس": row.get("نتیجه تماس", ""),
                            "ساعت_تماس_بعدی": row.get("ساعت تماس بعدی", ""),
                            "وضعیت_درخواست_مشتری": row.get("وضعیت درخواست مشتری", ""),
                            "پیام_رسان_نمونه_کار": row.get("پیام رسان نمونه کار", ""),
                            "توضیحات_نمونه_کار": row.get("توضیحات نمونه کار", ""),
                            "وضعیت_ارسال": row.get("وضعیت ارسال", ""),
                            "پیغام_مدیر": row.get("پیغام مدیر", ""),
                            "زمان_تمدید": row.get("زمان تمدید", ""),
                        },
                    )
                    count += 1

            self.stdout.write(self.style.SUCCESS(f"✅ وارد شدند: {count} رکورد"))

        except FileNotFoundError:
            self.stdout.write(self.style.ERROR(f"❌ فایل یافت نشد: {csv_path}"))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"❌ خطا در ایمپورت: {e}"))
