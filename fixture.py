import csv
from tortoise import Tortoise, run_async
from core.constants import TORTOISE_ORM
from models import Company, CompanyName, Tag, TagName


def make_company_names(row: dict) -> list:
    ret = []
    keys = ['company_ko', 'company_en', 'company_ja']
    for k in keys:
        if row.get(k):
            ret.append({
                'language': k.replace('company_', '').upper(),
                'name': row.get(k)
            })

    return ret


def make_tag_names(row: dict):
    ret = []
    keys = ['tag_ko', 'tag_en', 'tag_ja']
    tags = {
        'KO': [],
        'EN': [],
        'JA': []
    }

    for k in keys:
        if row.get(k):
            locale = k.replace('tag_', '').upper()
            tags[locale] += row.get(k).split('|')

    locales = ['KO', 'EN', 'JA']
    for i in range(0, len(tags.get('KO'))):
        ap = []
        for l in locales:
            ap.append({'language': l, 'name': tags.get(l)[i]})

        ret.append(ap)

    return ret


async def run():
    await Tortoise.init(TORTOISE_ORM)
    await tags()

    f = open('wanted_temp_data.csv', 'r', encoding='utf-8')
    line = 0
    for r in csv.DictReader(f):
        line += 1
        if line == 1:
            continue
        names = make_company_names(r)
        # print(line, r, names)

        company = await Company.create()
        for n in names:
            await CompanyName.create(
                company=company,
                language=n.get('language'),
                name=n.get('name')
            )

        for t in await Tag.filter(names__name__in=r.get('tag_en').split('|')).all():
            await company.tags.add(t)


async def tags():
    f = open('wanted_temp_data.csv', 'r', encoding='utf-8')
    line = 0
    for r in csv.DictReader(f):
        line += 1
        if line == 1:
            continue

        for t in make_tag_names(r):
            tag = await Tag.create()
            for tn in t:
                chk = await TagName.get_or_none(name=tn.get('name'))
                if chk is None:
                    await TagName.create(
                        tag=tag,
                        language=tn.get('language'),
                        name=tn.get('name')
                    )


if __name__ == "__main__":
    run_async(run())