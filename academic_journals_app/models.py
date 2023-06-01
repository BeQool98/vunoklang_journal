from django.db import models
from taggit.managers import TaggableManager
from ckeditor_uploader.fields import RichTextUploadingField
from django.urls import reverse

# Create your models here.

#Create your User model her if necessary
class User(models.Model):
    author = models.CharField(max_length=50)

    # class Meta:
    #     verbose_name = "User"
    #     verbose_plural = "Users"
    
    def __str__(self):
        return self.author
#Book Model

class Owner_Details(models.Model):
    meta_author = models.CharField(max_length=200, null=True,blank=True, help_text="Seo author name")
    meta_description = models.CharField(max_length=200, null=True,blank=True, help_text="Seo description")
    meta_keywords = models.TextField(null=True,blank=True, help_text="Seo keywords" )
    title=models.CharField(max_length=200, null=True, blank=True, default="My site", help_text="Name of your site")
    favicon = models.ImageField(null=True, blank=True, help_text="image that appears on your url")
    logo = models.ImageField(null=True, blank=True, help_text="Logo that appears on your site")
    site_description = models.CharField(max_length=300, null=True, blank=True, help_text="A logo alternative in written form")
    footer_title = models.CharField(max_length=300, null=True, blank=True, help_text="Your footer title")
    footer_description = models.CharField(max_length=300, null=True, blank=True, help_text="Your footer description")
    facebook= models.URLField(null=True, blank=True, help_text="Facebook url")
    Twitter= models.URLField(null=True, blank=True, help_text="Twitter url")
    Instagram= models.URLField(null=True, blank=True, help_text="Instagram url")
    linkedIn= models.URLField(null=True, blank=True, help_text="Linkedin url")
    Address = models.CharField(max_length=1000, null=True, blank=True, help_text="Your Address")
    Tel = models.IntegerField(null=True, blank=True,help_text="Your phone number")
    Email = models.EmailField(null=True, blank=True,help_text="Your Email Address")
    Working_hours = models.CharField(max_length=300, null=True, blank=True, help_text="Your specific working hours")

    class Meta:
        verbose_name = "Owner_Detail"
        verbose_name_plural = "Owner_Details"

    def __str__(self) -> str:
        return f"Website: {self.title} | Owner: {self.meta_author}"
    
class Comment_Email(models.Model):
    name=models.CharField(max_length=400, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)

    def __str__(self):
        return f"Commenter: {self.name} | Email: {self.email}"

STATUS = (
    ("Draft", "Draft"),
    ("Published", "Published")
    
)



class Category(models.Model): #Category for the Article
    title = models.CharField(max_length=200) #Title of the Category
    created_on = models.DateTimeField(auto_now_add=True) #Date of creation

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"
        ordering = ['title']

    def __str__(self):
        return self.title

class BookDetailPost(models.Model):
    title = models.CharField(max_length=200, unique=True, help_text="The name of your book") #Title of the Article
    slug = models.SlugField(max_length=200, unique=True,help_text="Re-type the name of your book", null=True, blank=True) #Unique identifier for the article
    author = models.CharField( max_length=250,null=True, blank=True) #Author of the Article
    description = models.TextField(help_text="A short description of your book") #Short Description of the article
    quote = models.CharField(max_length=300, null=True, blank=True)
    # content = RichTextUploadingField(config_name='awesome_ckeditor') #Content of the article, you need to install CKEditor
    # tags = TaggableManager() #Tags for a Particular Article, You need to install Taggit
    category = models.ForeignKey(Category, related_name='category', on_delete=models.SET_NULL,null=True, blank=True, help_text="Choose the ctegory your book fall in.") #Category of the article
    keywords = models.CharField(max_length=250, help_text="Choose keywords to locate your book easier", null=True, blank=True) #Keywords to be used in SEO
    cover = models.ImageField(upload_to='book_covers/', null=True, blank=True) #Cover Image of the article
    book = models.FileField(upload_to='books/',null=True, help_text='Upload your book here')# The book
    created_on = models.DateTimeField(auto_now_add=True) #Date of creation
    updated_on = models.DateTimeField(auto_now=True) #Date of updation
    status = models.CharField(choices=STATUS, max_length=200, default="Published") #Status of the Article either Draft or Published

    def __str__(self):
        return self.title
    
    def get_total_comments(self):
        return Comment.objects.filter(comment=self).count() 

    def get_absolute_url(self):
        return reverse("book_detail", args=[str(self.slug)])

    
class AboutPage(models.Model):
    header= models.CharField(max_length=200, null=True, blank=True, help_text="add the header")
    body=models.TextField(null=True, blank=True)
    
    def __str__(self):
        return self.header
    
    
class EditorialMembers(models.Model):
    name=models.CharField(max_length=200, null=True, blank=True)
    department=models.CharField(max_length=200, null=True, blank=True)
    consulting_editor=models.BooleanField(default=False)
    if name is not None:
        def __str__(self):
            return self.name
    
    
class ContactUs(models.Model):
    name=models.CharField(max_length=200,null=True, blank=True)
    email=models.CharField(max_length=200,null=True, blank=True)
    subject=models.CharField(max_length=200,null=True, blank=True)
    messagename=models.TextField()
    
    if name is not None:
        def __str__(self):
            return self.name
        

class AboutHeaders(models.Model):
    main_header=models.CharField(max_length=100, null=True, blank=True)
    second_header=models.CharField(max_length=200, null=True, blank=True)
    volume=models.CharField(max_length=50, null=True, blank=True)
    header_image1=models.ImageField(null=True, blank=True)
    header_image2=models.ImageField(null=True, blank=True)
    
    
    def __str__(self):
        return self.main_header
    




class Comment(models.Model):
    comment = models.ForeignKey(BookDetailPost, related_name="comments", help_text="Numberof comments in a post", on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=200, help_text="Name of the person making a comment", null=True, blank=True)
    email = models.EmailField(help_text="Email of the person making a comment", null=True, blank=True)
    description = models.TextField(help_text="The comment made", null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True, help_text="Date created", null=True, blank=True)

    def __str__(self):
        return f"{self.comment.title} | {self.name}"

