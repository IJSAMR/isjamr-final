from datetime import datetime
from django.forms import ValidationError
from django.utils import timezone
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils.translation import gettext_lazy as _
from .managers import CustomUserManager

# Create your models here.


class User(AbstractBaseUser, PermissionsMixin):
    first_name = models.CharField(_("First Name"), max_length=100)
    last_name = models.CharField(_("Last Name"), max_length=100)
    email = models.EmailField(_("Email Address"), max_length=254, unique=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    date_joined =  models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name"]

    objects = CustomUserManager()

    class Meta:
        verbose_name = _("User")
        verbose_name_plural = _("Users")

    def __str__(self):
        return self.email
    
    @property
    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"


class Article(models.Model):
    SUBMITTED = 'submitted'
    UNDER_REVIEW = 'under review'
    APPROVED = 'approved'
    REJECTED = 'rejected'
    PUBLISHED = 'published'

    STATUS_CHOICES = [
        (SUBMITTED, 'Submitted'),
        (UNDER_REVIEW, 'Under Review'),
        (APPROVED, 'Approved'),
        (REJECTED, 'Rejected'),
        (PUBLISHED, 'Published'),
    ]
    submitted_by = models.ForeignKey(User,models.CASCADE,related_name='articles')
    unique_id = models.CharField(max_length=20, unique=True, editable=False)
    submission_year = models.PositiveIntegerField(default=timezone.now().year)
    author_name = models.CharField(max_length=255)
    author_email =models.EmailField()
    author_phone = models.CharField(max_length=10)
    co_authors= models.JSONField(null=True,blank=True)
    title = models.CharField(max_length=255)
    address = models.CharField(max_length=500)
    subject=models.CharField(max_length=100)
    abstract = models.TextField()
    article_pdf = models.FileField(upload_to='article_pdf/',null=True,blank=True)
    article_doc = models.FileField(upload_to="article_doc/",null=True,blank=True)
    article_copyright=models.FileField(upload_to='copyright_form/',null=True,blank=True) # needs to be file
    status = models.CharField(max_length=20,choices=STATUS_CHOICES,default=STATUS_CHOICES[0])
    submitted_date = models.DateTimeField(null=True,blank=True)
    approved_date = models.DateField(null=True,blank=True)


    def save(self, *args, **kwargs):

        # Ensure that approved_date is set only when the status is 'approved'
        if self.status == "approved" and not self.approved_date:
            # self.approved_date =datetime.fromisoformat(timezone.now().date)
            self.approved_date=timezone.now().date()
            print(f"Article with id {self.unique_id} approved on {self.approved_date}")
            # print(f"Article with id {self.unique_id} approved on {self.approved_date.strfdate('%d-%m-%Y')}")

            # print(timezone.now())
        elif self.status != 'approved' and self.status !='published':
            self.approved_date = None

        # Unique ID generation logic
        if not self.unique_id:
            year = self.submission_year
            article_count = Article.objects.filter(submission_year=year).count() + 1
            self.submited_date=timezone.now()
            while True:
                self.unique_id = f"ISJAMR{year}{article_count:04d}"
                if not Article.objects.filter(unique_id=self.unique_id).exists():
                    break
                article_count += 1
        if(self.status == "submitted" and not self.submitted_date):
            self.submitted_date= timezone.now()
            print(f"Article with id {self.unique_id} submitted on {self.submitted_date}")
        
        super().save(*args, **kwargs)
    def __str__(self):
        return self.unique_id

#model for issues
class Issue(models.Model):
    article_id = models.ForeignKey(Article,models.CASCADE,related_name='issues')
    issue_title = models.CharField(max_length=255)
    vol_no = models.IntegerField()
    issue_no = models.IntegerField()
    year = models.BigIntegerField()
    month = models.CharField(max_length=20)
    issued_date=models.DateField(null=True,blank=True)
    newIssuePdf = models.FileField(upload_to="issues_pdf/",null=True,blank=True)

    def clean(self):
        # Custom validation to ensure the associated article is approved
        if self.article_id.status != Article.APPROVED:
            raise ValidationError(
                {'article_id': f"Cannot create an issue for an article with status '{self.article_id.status}'. Only approved articles can be issued."}
            )

    def save(self, *args, **kwargs):
        # Call the clean method to ensure validation is performed
        if self.article_id.status == Article.APPROVED:
            self.article_id.status = Article.PUBLISHED
            self.issued_date=timezone.now().date()
            self.article_id.save()  # Save the article to update its status

        # super().save(*args, **kwargs)
        print(f"Article with id {self.article_id.unique_id} has {self.article_id.status} on {self.issued_date}")
        super().save(*args, **kwargs)

    def __str__(self):
        return (self.article_id.unique_id+" "+self.issue_title)
    

# model for new anouncements
class Announcements(models.Model):
    title=models.CharField(max_length=500)
    description = models.TextField(max_length=1000)
    bochure_pdf = models.FileField(upload_to="bochure_pdf/",null=True,blank=True)

    def __str__(self):
        return (self.title)


#model for reviewers list

class Reviewer(models.Model):
    reviewer_name = models.CharField(max_length=100)

    def __str__(self):
        return (self.reviewer_name)