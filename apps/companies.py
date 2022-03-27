from typing import List, Optional
from fastapi import APIRouter, Response
from starlette.status import HTTP_201_CREATED, HTTP_204_NO_CONTENT
from models import (Company, Company_Pydantic, CompanyName, CompanyName_Pydantic, Tag)


router = APIRouter()

@router.get('/companies', name='company.list', response_model=List[Company_Pydantic])
async def company_list(name: Optional[str] = None, tag_name: Optional[str] = None):
    filters = {}
    if name:
        filters['names__name__icontains'] = name
    if tag_name:
        filters['tags__names__name__icontains'] = tag_name

    companies = Company.all().filter(**filters).prefetch_related('names', 'tags__names')
    return await Company_Pydantic.from_queryset(companies)


@router.get('/companies-names', name='companyName.list', response_model=List[CompanyName_Pydantic])
async def company_name_autocomplete(keyword: Optional[str]):
    company_names = CompanyName.filter(name__icontains=keyword).all()
    return await CompanyName_Pydantic.from_queryset(company_names)


@router.get('/companies/{id}', response_model=Company_Pydantic)
async def company_show(id: int):
    queryset = Company.get(id=id).prefetch_related('names', 'tags__names')
    return await Company_Pydantic.from_queryset_single(queryset)


@router.post('/companies/{id}/tags', response_model=Company_Pydantic)
async def add_tags(id: int, tag_ids: List[int]):
    company = await Company.get(id=id)
    tags = await Tag.filter(id__in=tag_ids).all()
    await company.tags.add(*tags)

    queryset = Company.get(id=id).prefetch_related('names', 'tags__names')
    return await Company_Pydantic.from_queryset_single(queryset)


@router.delete('/companies/{id}/tags', response_model=Company_Pydantic)
async def remove_tags(id: int, tag_ids: List[int]):
    company = await Company.get(id=id)
    for t in await company.tags.filter(id__in=tag_ids).all():
        await company.tags.remove(t)

    queryset = Company.get(id=id).prefetch_related('names', 'tags__names')
    return await Company_Pydantic.from_queryset_single(queryset)
    
