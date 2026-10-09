"""Reviewed coverage additions, pronunciation aliases and explicit field contexts.
Applied AFTER historical deduplication: a shared concept must remain discoverable
in each explicitly reviewed field. Definitions may be identical; examples aren't.
"""
from pathlib import Path
import json,collections,copy
ROOT=Path(__file__).parent
DATE='2026-10-07'
BATCH='coverage-2026-10-07'
SOURCES={
 'cov-lamination':('CCLIM 클림','패브릭 가방 원단 선정과 공정 설계','https://cclim.kr/blog/0af87e2f-928d-4308-bd1d-5a699689f1ed/'),
 'cov-packing':('품고','합포장 안내','https://welcome.poomgo.com/6c0d752a-6605-435a-872b-ac2cff811c85'),
 'cov-ir':('Samsung Electronics','4Q 2025 Results — YoY / QoQ usage','https://images.samsung.com/is/content/samsung/assets/global/ir/docs/2025_4Q_conference_eng.pdf'),
 'cov-period':('Oracle','Accounting Calendar Time Periods','https://docs.oracle.com/en/cloud/saas/sales/farig/use-the-accounting-calendar-time-periods-for-your-rollups.html'),
 'cov-cashflow':('IFRS Foundation','IAS 7 Statement of Cash Flows','https://www.ifrs.org/issued-standards/list-of-standards/ias-7-statement-of-cash-flows/'),
 'cov-sec':('SEC','Small Business Glossary','https://www.sec.gov/resources-small-businesses/glossary'),
 'cov-nongaap':('SEC','Financial Reporting Manual — Non-GAAP Measures','https://www.sec.gov/about/divisions-offices/division-corporation-finance/financial-reporting-manual/frm-topic-8'),
 'cov-fpa':('Oracle','What is FP&A?','https://www.oracle.com/performance-management/planning/what-is-fp-and-a/'),
 'cov-variance':('Oracle','Variance/Var','https://docs.oracle.com/en/cloud/saas/planning-budgeting-cloud/pfusa/variance_var.html'),
 'cov-forecast':('Oracle','Forecasting Basics','https://docs.oracle.com/en/cloud/saas/planning-budgeting-cloud/pfusu/forecasting_basics_100xdcac5107.html'),
 'cov-working':('SAP','Working Capital Management','https://learning.sap.com/de/courses/exploring-sap-taulia-working-capital-management/explaining-the-importance-of-working-capital-management'),
 'cov-fte':('SAP','FTE (Full-Time Equivalent)','https://help.sap.com/docs/BI_CONTENT_747/d26cb97cca534166b0cd52f94e935524/e279895360b93d58e10000000a174cb4.html'),
 'cov-hire':('Greenhouse','What is time-to-hire?','https://www.greenhouse.com/resources/glossary/what-is-time-to-hire'),
 'cov-talent':('Workday','Talent Management in HR','https://www.workday.com/en-gb/topics/hr/talent-management-hr.html'),
 'cov-hrmetrics':('SAP','Human Resources Dashboard','https://help.sap.com/docs/PRODUCT_ID/2754875d2d2a403f95e58a41a9c7d6de/2d1ab918722d1014b8ffc221e7ae5a2e.html?locale=en-US&state=PRODUCTION&version=2111'),
 'cov-hris':('Workday','What Is an HRIS?','https://www.workday.com/en-us/topics/hr/hris.html'),
 'cov-compa':('SAP','Calculating Salary Benchmarks','https://learning.sap.com/courses/sap-successfactors-compensation-project-team-orientation/calculating-salary-benchmarks'),
 'cov-ebitda-usage':('YTN 라디오','EBITDA의 에비따 발음 사용 사례','https://m.radio.ytn.co.kr/interview_view.php?id=108366&s_mcd=0206'),
 'cov-roas':('Google Ads','타겟 ROAS 입찰','https://support.google.com/google-ads/answer/6268637?hl=ko'),
 'cov-opt':('Google Ads','최적화 점수 소개','https://support.google.com/google-ads/answer/9061546?hl=ko'),
 'cov-delay':('Google Ads','실적 최대화 캠페인 결과 평가','https://support.google.com/google-ads/answer/16279166?hl=ko'),
 'cov-debounce':('MDN','Debounce','https://developer.mozilla.org/en-US/docs/Glossary/Debounce'),
 'cov-shutter':('ARRI','Electronic and Mirror Shutter White Paper','https://www.arri.com/resource/blob/178016/ad23969317dafff402f0902d47bb4ab7/alexa-studio-electronic-and-mirror-shutter-white-paper-data.pdf'),
 'cov-components':('Figma','Components in Figma','https://www.figma.com/blog/components-in-figma/'),
 'cov-constraints':('Figma','Tips for using Constraints','https://www.figma.com/best-practices/tips-for-using-constraints-in-your-workflow/'),
}

def candidates():
 field=category=''
 for number,line in enumerate((ROOT/'coverage_expansion.tsv').read_text().splitlines(),1):
  if not line:continue
  if line.startswith('# '):field,category=line[2:].split('|');continue
  parts=line.split('|');assert len(parts)==6,(number,parts)
  term,english,aliases,definition,example,source=parts
  yield dict(field=field,category=category,term=term,english=english,aliases=[x for x in aliases.split(';') if x],definition=definition,example=example,sources=[source] if source else [],kind='현장 표현' if '현장 말' in category else '전문 용어')

def apply(entries,sources,id_map):
 sources.update({k:dict(id=k,publisher=v[0],title=v[1],url=v[2],published='',historical=False,checkedAt=DATE) for k,v in SOURCES.items()})
 index={(e['field'],e['term']):e for e in entries}
 counts=collections.Counter()
 for value in id_map.values():
  f,num=value.rsplit('-',1);counts[f]=max(counts[f],int(num))
 def add(row):
  key=row['field'],row['term'];assert key not in index,('Coverage duplicate',key)
  identity='|'.join(key)
  if identity not in id_map:
   counts[key[0]]+=1;id_map[identity]=key[0]+'-'+str(counts[key[0]]).zfill(3)
  e=dict(row,id=id_map[identity],note=row.get('note',''),phrases=row.get('phrases',[row['definition']]),historical=False,checkedAt=DATE if row['sources'] else '',evidence='')
  e['evidence']='복수 자료 대조' if len(e['sources'])>1 else '공개 자료 확인' if e['sources'] else '일반 지식 기반 · 외부 출처 미첨부'
  if not e['sources']:e['writtenAt']=DATE
  entries.append(e);index[key]=e
 for row in candidates():add(row)
 for update in json.loads((ROOT/'coverage_aliases.json').read_text()):
  key=update['field'],update['term'];assert key in index,('Unknown alias target',key)
  e=index[key];e['aliases']=list(dict.fromkeys(e['aliases']+update['aliases']))
  for prop in ['english','note']:
   if prop in update:e[prop]=update[prop]
  if 'sources' in update:
   e['sources']=list(dict.fromkeys(e['sources']+update['sources']));e.update(checkedAt=DATE,evidence='복수 자료 대조' if len(e['sources'])>1 else '공개 자료 확인');e.pop('writtenAt',None)
 # Same concept: preserve the reviewed definition and source, but author a real
 # example for EACH context. Never mass-copy an ad example into clothing or IT.
 fields=['marketing','dev','fashion','film','design','hrfinance']
 labels={'marketing':'광고','dev':'개발','fashion':'패션','film':'영상 제작','design':'디자인','hrfinance':'인사·재무'}
 for number,line in enumerate((ROOT/'shared_contexts.tsv').read_text().splitlines(),1):
  if not line or line.startswith('#'):continue
  cells=line.split('|');assert len(cells)==7,(number,cells)
  term=cells[0];canonical=index['common',term]
  for f,example in zip(fields,cells[1:]):
   if example=='-' or (f,term) in index:continue
   row={k:copy.deepcopy(canonical[k]) for k in ['term','english','aliases','definition','kind','sources','note']}
   row.update(field=f,example=example,category=labels[f]+' 협업·회의',phrases=[example,canonical['definition']])
   add(row)
 return entries
