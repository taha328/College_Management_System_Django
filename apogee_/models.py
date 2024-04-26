# college_app/models.py
from django.db import models
from reportlab.lib.pagesizes import letter
from django.db.models import Sum, Avg
from django.contrib.auth.models import User
from io import BytesIO
from reportlab.pdfgen import canvas
from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator

class DossierEtudiant(models.Model):
    SEXE_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        # Add other choices as needed
    ]

    CURSUS_CHOICES = [
        ('deug', 'Deug'),
        ('deust', 'Deust'),
        ('deup', 'Deup'),
        ('dut', 'Dut'),
        # Add other choices as needed
    ]
    CHOICES_ = [
        ('deust', 'Deust'),
        ('licence', 'Licence'),
        ('cycle dingénieur', 'Cycle dingénieur'),
        ('master', 'Master'),
        
        # Add other choices as needed
    ]
    
    nom = models.CharField(max_length=50, null=True, blank=True)
    prenom = models.CharField(max_length=50, null=True, blank=True)
    cin = models.CharField(max_length=20, unique=True, null=True, blank=True)
    Cne = models.CharField(max_length=20, primary_key=True)

    sexe = models.CharField(max_length=1, choices=SEXE_CHOICES, null=True, blank=True)
    numero_tele = models.CharField(max_length=15, null=True, blank=True)
    ville = models.CharField(max_length=50, null=True, blank=True)
    email = models.EmailField( null=True, blank=True)

    Dernier_diplome_obtenu = models.CharField(max_length=20, choices=CURSUS_CHOICES, null=True, blank=True)
    adresse = models.TextField( max_length=255,default="Votre adresse")
    Formation_souhaitée = models.CharField(max_length=30, choices=CHOICES_, null=True, blank=True)

    # Fields for notes from S1 to S6
    note_s1 = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    note_s2 = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    note_s3 = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    note_s4 = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    note_s5 = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    note_s6 = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)

    transcript = models.FileField(upload_to='transcripts/', null=True, blank=True)

    def __str__(self):
        return f"{self.Cne}"

    def get_transcript_download_url(self):
        if self.transcript:
            return self.transcript.url
        return None

class Stage(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    convention_stage = models.TextField(default="Default Convention Stage")
    entreprise = models.CharField(max_length=255, null=True, blank=True)
    periode_de_stage = models.CharField(max_length=100, null=True, blank=True)
    adresse_d_entreprise = models.TextField(null=True, blank=True)

    
    def generate_pdf(self, etudiant):
        buffer = BytesIO()

        # Create a PDF document
        pdf = canvas.Canvas(buffer, pagesize=letter)

        # Add information to the PDF
        pdf.drawString(100, 800, f"Username: {self.user.username}")
        pdf.drawString(100, 780, f"Convention Stage: {self.convention_stage}")
        pdf.drawString(100, 760, f"Entreprise: {self.entreprise}")
        pdf.drawString(100, 740, f"Période de Stage: {self.periode_de_stage}")
        pdf.drawString(100, 720, f"Adresse d'Entreprise: {self.adresse_d_entreprise}")
        pdf.drawString(100, 700, f"Cycle: {etudiant.inscriptions.last().cycle}")

        # Include additional information (modify as needed)

        # Save the PDF content
        pdf.save()

        # Set the buffer position to the beginning
        buffer.seek(0)

        return buffer

    def save(self, *args, **kwargs):
        self.convention_stage = self.convention_stage or "Default Convention Stage"
        super().save(*args, **kwargs)

        etudiant = self.user
        pdf_buffer = self.generate_pdf(etudiant)
        pdf_file_path = f"stage_{self.pk}_document.pdf"

        with open(pdf_file_path, "wb") as pdf_file:
            pdf_file.write(pdf_buffer.read())
class Coefficient(models.Model):
    matiere = models.ForeignKey('Matiere', on_delete=models.CASCADE)
    value = models.FloatField()

    def __str__(self):
        return f'{self.matiere} - Coefficient: {self.value}'

class ControleConnaissances(models.Model):
    
    coefficients = models.ForeignKey(Coefficient, on_delete=models.CASCADE)
    règles_calcul = models.TextField()

    def __str__(self):
        return f'{self.coefficients}'
class Resultat(models.Model):
    etudiant = models.ForeignKey(User, on_delete=models.CASCADE)
    matiere = models.ForeignKey('Matiere', on_delete=models.CASCADE)
    notes = models.DecimalField(max_digits=5, decimal_places=2)  
    classement = models.IntegerField(null=True, blank=True)
    moyennes = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    def save(self, *args, **kwargs):
        # Calculate the average when saving the Resultat object
        existing_notes = Resultat.objects.filter(etudiant=self.etudiant).exclude(notes=None).exclude(pk=self.pk)
        matieres_count = existing_notes.count()
        total_notes = existing_notes.aggregate(Sum('notes'))['notes__sum']

        if self.notes is not None:
            # If the current instance has non-None notes, include it in the calculation
            if total_notes is not None:
                total_notes += self.notes
            else:
                total_notes = self.notes

        self.moyennes = total_notes / matieres_count if matieres_count > 0 else None

        # Update classement based on moyennes
        self.classement = self.get_student_classement()

        super().save(*args, **kwargs)

    def get_student_classement(self):
        # Get the rank of the student based on moyennes
        students = Resultat.objects.filter(moyennes__isnull=False).values('etudiant').annotate(avg_moyennes=Avg('moyennes')).order_by('-avg_moyennes')

        for index, student in enumerate(students):
            if student['etudiant'] == self.etudiant:
                return index + 1  # Rank starts from 1

        return None

    def __str__(self):
        return str(self.etudiant)
class Professeur(models.Model):
    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)
    # Add other fields for Professeur
    def __str__(self):
        return self.nom    

class Matiere(models.Model):
    nom = models.CharField(max_length=100)
    professeur = models.ForeignKey(Professeur, on_delete=models.CASCADE, default=1)
    def __str__(self):
        return self.nom

class Cycle(models.Model):
    CYCLE_CHOICES = [
        ('preparatoire', 'Préparatoire'),
        ('licence', 'Licence'),
        ('ingenieur', 'Ingénieur'),
        ('master', 'Master'),
        ('doctorat', 'Doctorat'),
    ]

    cyclee = models.CharField(max_length=20, choices=CYCLE_CHOICES, default='preparatoire')
    

    # Add other fields for Filiere

    def __str__(self):
        return f'{self.get_cyclee_display()} - {self.id}'

# Create instances for "mipc" and "bcg" majors


class InscriptionPédagogique(models.Model):
    matiere = models.ForeignKey(Matiere, on_delete=models.CASCADE, default=1, related_name='inscriptions')
    cycle = models.ForeignKey(Cycle, on_delete=models.CASCADE, default=1, related_name='inscriptions')
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, default=1, related_name='inscriptions')

    def __str__(self):
        return f'{self.user} - {self.matiere.nom} - {self.cycle.get_cyclee_display()}'