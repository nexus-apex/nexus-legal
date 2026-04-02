from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from core.models import LegalCase, LegalClient, LegalTimeEntry
from datetime import date, timedelta
import random


class Command(BaseCommand):
    help = 'Seed NexusLegal with demo data'

    def handle(self, *args, **kwargs):
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser('admin', 'admin@nexuslegal.com', 'Admin@2024')
            self.stdout.write(self.style.SUCCESS('Admin user created'))

        if LegalCase.objects.count() == 0:
            for i in range(10):
                LegalCase.objects.create(
                    title=f"Sample LegalCase {i+1}",
                    case_number=f"Sample {i+1}",
                    client_name=f"Sample LegalCase {i+1}",
                    case_type=random.choice(["civil", "criminal", "corporate", "family", "ip", "labor"]),
                    status=random.choice(["open", "in_progress", "hearing", "settled", "closed"]),
                    court=f"Sample {i+1}",
                    next_hearing=date.today() - timedelta(days=random.randint(0, 90)),
                )
            self.stdout.write(self.style.SUCCESS('10 LegalCase records created'))

        if LegalClient.objects.count() == 0:
            for i in range(10):
                LegalClient.objects.create(
                    name=["Rajesh Kumar","Priya Sharma","Amit Patel","Deepa Nair","Vikram Singh","Ananya Reddy","Suresh Iyer","Meera Joshi","Karthik Rao","Fatima Khan"][i],
                    email=f"demo{i+1}@example.com",
                    phone=f"+91-98765{43210+i}",
                    client_type=random.choice(["individual", "corporate"]),
                    company=["TechVision Pvt Ltd","Global Solutions","Pinnacle Systems","Nova Enterprises","CloudNine Solutions","MetaForge Inc","DataPulse Analytics","QuantumLeap Tech","SkyBridge Corp","Zenith Innovations"][i],
                    active_cases=random.randint(1, 100),
                    total_billed=round(random.uniform(1000, 50000), 2),
                    retainer=random.choice([True, False]),
                )
            self.stdout.write(self.style.SUCCESS('10 LegalClient records created'))

        if LegalTimeEntry.objects.count() == 0:
            for i in range(10):
                LegalTimeEntry.objects.create(
                    case_title=f"Sample LegalTimeEntry {i+1}",
                    attorney=f"Sample {i+1}",
                    hours=round(random.uniform(1000, 50000), 2),
                    rate=round(random.uniform(1000, 50000), 2),
                    amount=round(random.uniform(1000, 50000), 2),
                    date=date.today() - timedelta(days=random.randint(0, 90)),
                    activity=random.choice(["research", "drafting", "court", "meeting", "review"]),
                    description=f"Sample description for record {i+1}",
                    billable=random.choice([True, False]),
                )
            self.stdout.write(self.style.SUCCESS('10 LegalTimeEntry records created'))
