from tortoise import Tortoise, fields
from tortoise.contrib.pydantic import pydantic_model_creator
from core.constants import Language
from core.models import BaseModel, TimeStampMixin


class Post(BaseModel, TimeStampMixin):
    title = fields.CharField(max_length=255)
    body = fields.TextField()

    class Meta:
        table = 'posts'
        ordering = ['-id']

    def __str__(self):
        return self.id


class CompanyName(BaseModel, TimeStampMixin):
    company: fields.ForeignKeyRelation['Company'] = fields.ForeignKeyField(
        'models.Company',
        related_name='names',
        db_constraint=False,
    )
    language: Language = fields.CharEnumField(Language, default=Language.KOREA)
    name = fields.CharField(max_length=255)

    class Meta:
        table = 'company_names'
    
    class PydanticMeta:
        # computed = ["full_name"]
        exclude = ['created_at', 'updated_at']

    def __str__(self):
        return self.id


class Company(BaseModel, TimeStampMixin):
    names: fields.ReverseRelation['CompanyName']
    tags: fields.ManyToManyRelation["Tag"] = fields.ManyToManyField(
        "models.Tag", related_name="tags", through="companies_tags"
    )

    class Meta:
        table = 'companies'

    def __str__(self):
        return self.id


class Tag(BaseModel, TimeStampMixin):
    names: fields.ReverseRelation['TagName']
    companies: fields.ManyToManyRelation['Company']

    class Meta:
        table = 'tags'

    class PydanticMeta:
        exclude = ['created_at', 'updated_at']

    def __str__(self):
        return self.id


class TagName(BaseModel, TimeStampMixin):
    tag: fields.ForeignKeyRelation[Tag] = fields.ForeignKeyField(
        'models.Tag',
        related_name='names',
        db_constraint=False,
    )
    language: Language = fields.CharEnumField(Language, default=Language.KOREA)
    name = fields.CharField(max_length=255)

    class Meta:
        table = 'tag_names'

    class PydanticMeta:
        exclude = ['created_at', 'updated_at']

    def __str__(self):
        return self.id


Tortoise.init_models(['models'], 'models')

Post_Pydantic = pydantic_model_creator(Post, name="Post")
PostIn_Pydantic = pydantic_model_creator(Post, name="PostIn", exclude_readonly=True)

Company_Pydantic = pydantic_model_creator(Company)
CompanyIn_Pydantic = pydantic_model_creator(Company, name="CompanyIn", exclude_readonly=True)

CompanyName_Pydantic = pydantic_model_creator(CompanyName, name="CompanyName")
CompanyNameIn_Pydantic = pydantic_model_creator(CompanyName, name="CompanyNameIn", exclude_readonly=True)

Tag_Pydantic = pydantic_model_creator(Tag, name="Tag")
TagIn_Pydantic = pydantic_model_creator(Tag, name="TagIn", exclude_readonly=True)

TagName_Pydantic = pydantic_model_creator(TagName, name="TagName")
TagNameIn_Pydantic = pydantic_model_creator(TagName, name="TagNameIn", exclude_readonly=True)