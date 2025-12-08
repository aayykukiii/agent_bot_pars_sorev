import asyncio
import aiohttp 
from bs4 import BeautifulSoup
import re



#парс первого сайта
async def parse_habr_career(url):
    """Parse career.habr.com and return list of vacancy dicts."""
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
        }

        async with aiohttp.ClientSession(headers=headers) as session:
            async with session.get(url) as response:
                if response.status != 200:
                    return []

                html = await response.text()
                soup = BeautifulSoup(html, 'html.parser')

                vacancies = soup.find_all('div', class_='vacancy-card')
                if not vacancies:
                    vacancies = soup.find_all('article', class_='vacancy-card')
                if not vacancies:
                    vacancies = soup.find_all('div', class_='vacancy-card__inner')

                results = []
                for i, vacancy in enumerate(vacancies, 1):
                    try:
                        title_elem = vacancy.find('a', class_='vacancy-card__title-link')
                        if not title_elem:
                            title_elem = vacancy.find('a', class_='vacancy-card__title')
                        if not title_elem:
                            title_elem = vacancy.find('h3')
                        if not title_elem:
                            title_elem = vacancy.find('a', attrs={'data-test': 'vacancy-card-title'})

                        title = title_elem.text.strip() if title_elem else 'Нет названия'

                        link = title_elem['href'] if title_elem and title_elem.has_attr('href') else '#'
                        if link and link.startswith('/'):
                            full_link = f'https://career.habr.com{link}'
                        elif link == '#':
                            full_link = '#'
                        else:
                            full_link = link

                        company_elem = vacancy.find('div', class_='vacancy-card__company-title')
                        if not company_elem:
                            company_elem = vacancy.find('a', class_='vacancy-card__company')
                        if not company_elem:
                            company_elem = vacancy.find('div', class_='company-name')
                        if not company_elem:
                            company_container = vacancy.find('div', class_='vacancy-card__company')
                            if company_container:
                                company_elem = company_container.find('a') or company_container

                        company = company_elem.text.strip() if company_elem else 'Не указана'

                        salary_elem = vacancy.find('div', class_='vacancy-card__salary')
                        if not salary_elem:
                            salary_elem = vacancy.find('div', class_='basic-salary')
                        if not salary_elem:
                            salary_elem = vacancy.find('span', class_='salary')
                        if not salary_elem:
                            salary_text = vacancy.find(text=lambda t: '₽' in t or '$' in t or '€' in t or 'руб' in t.lower())
                            if salary_text:
                                salary_elem = salary_text.parent

                        salary = salary_elem.text.strip() if salary_elem else None

                        skills = []
                        skills_container = vacancy.find('div', class_='vacancy-card__skills')
                        if not skills_container:
                            skills_container = vacancy.find('div', class_='skills')
                        if not skills_container:
                            skills_container = vacancy.find('ul', class_='skills-list')

                        if skills_container:
                            skill_elems = skills_container.find_all('a', class_='skill')
                            if not skill_elems:
                                skill_elems = skills_container.find_all('li', class_='skill-item')
                            if not skill_elems:
                                skill_elems = skills_container.find_all('span', class_='skill')
                            if not skill_elems:
                                skill_elems = skills_container.find_all('a')

                            for skill in skill_elems:
                                skill_text = skill.text.strip()
                                if skill_text and len(skill_text) < 50:
                                    skills.append(skill_text)

                        salary_num = None
                        try:
                            digits = re.sub(r"\D", "", salary or "")
                            if digits:
                                salary_num = int(digits)
                        except Exception:
                            salary_num = None

                        results.append({
                            'title': title,
                            'description': company,
                            'salary': salary_num,
                            'url': full_link,
                            'skills': skills,
                        })
                    except Exception:
                        continue

                return results
    except Exception:
        return []


async def main():
    url = 'https://career.habr.com/vacancies'
    print("🔍 Начинаем парсинг career.habr.com...\n")
    count = await parse_habr_career(url)
    print(f"\n✅ Парсинг завершен. Обработано вакансий: {count}")

    
    
#парс второго сайта



async def pars_superjob_grozny(url):
    """Parse SuperJob Grozny page and return list of vacancy dicts."""
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        }

        async with aiohttp.ClientSession(headers=headers) as session:
            async with session.get(url) as response:
                if response.status != 200:
                    return []

                html = await response.text()
                soup = BeautifulSoup(html, 'html.parser')

                vacancies = soup.find_all('div', class_='f-test-search-result-item')
                if not vacancies:
                    all_divs = soup.find_all('div', class_=True)
                    for div in all_divs:
                        classes = ' '.join(div.get('class', []))
                        if 'vacancy' in classes.lower() or 'serp' in classes.lower():
                            vacancies.append(div)

                results = []
                for i, vacancy in enumerate(vacancies, 1):
                    try:
                        title_elem = vacancy.find('a', class_='_6Nb0L')
                        if not title_elem:
                            title_elem = vacancy.find('a', class_='_1IHWd')
                        if not title_elem:
                            title_elem = vacancy.find('h3')
                        if not title_elem:
                            all_links = vacancy.find_all('a')
                            for link in all_links:
                                text = link.text.strip()
                                if text and len(text) > 5 and not text.startswith('http'):
                                    title_elem = link
                                    break

                        title = title_elem.text.strip() if title_elem else 'Не указано'
                        if title == 'Не указано':
                            continue

                        if title_elem and title_elem.has_attr('href'):
                            link = title_elem['href']
                            if link.startswith('/'):
                                full_link = f'https://grozniy.superjob.ru{link}'
                            elif link.startswith('http'):
                                full_link = link
                            else:
                                full_link = f'https://grozniy.superjob.ru/{link}'
                        else:
                            full_link = '#'

                        company_elem = vacancy.find('span', class_='_3nMqD')
                        if not company_elem:
                            company_elem = vacancy.find('div', class_='_3TK1M')
                        if not company_elem:
                            company_elem = vacancy.find('span', class_='f-test-text-vacancy-item-company-name')
                        company = company_elem.text.strip() if company_elem else 'Не указана'

                        salary_elem = vacancy.find('span', class_='_2eYAG')
                        if not salary_elem:
                            salary_elem = vacancy.find('span', class_='_1h3Zg')
                        if not salary_elem:
                            salary_match = re.search(r'[\d\s–]+[₽$€€руб]|от\s+\d+|до\s+\d+', vacancy.text)
                            if salary_match:
                                salary_elem = BeautifulSoup(f'<span>{salary_match.group()}</span>', 'html.parser').span

                        salary = salary_elem.text.strip() if salary_elem else None

                        date_elem = vacancy.find('span', class_='f-test-text-datetime')
                        if not date_elem:
                            date_match = re.search(r'(сегодня|вчера|\d+\s+\w+ назад|\d+\.\d+\.\d+)', vacancy.text, re.IGNORECASE)
                            if date_match:
                                date_elem = BeautifulSoup(f'<span>{date_match.group()}</span>', 'html.parser').span
                        date = date_elem.text.strip() if date_elem else None

                        salary_num = None
                        try:
                            digits = re.sub(r"\D", "", salary or "")
                            if digits:
                                salary_num = int(digits)
                        except Exception:
                            salary_num = None

                        results.append({
                            'title': title,
                            'description': company,
                            'salary': salary_num,
                            'url': full_link,
                            'skills': [],
                        })
                    except Exception:
                        continue

                return results
    except Exception:
        return []


async def main():
    url = 'https://grozniy.superjob.ru/vacancy/search/?click_from=facet'
    print("=" * 70)
    print(f"\n🔍 Ищем вакансии.....")
    print("=" * 70)
    

    
    count = await pars_superjob_grozny(url)
    print(f"\n✅ Парсинг завершен. Обработано вакансий: {count}")