"""HR/finance workplace dictionary. Definitions and examples individually authored.
No rates, statutory deadlines or individualized legal/tax advice are encoded.
"""
from pathlib import Path
DATE='2026-10-07'
SOURCES={
 'hf-contract':('고용노동부','표준 근로계약서 작성 안내','https://www.moel.go.kr/mainpop2.do','',False),
 'hf-withholding':('국세청','원천징수 개요','https://t.nts.go.kr/nts/cm/cntnts/cntntsView.do?cntntsId=7701&mi=2413','',False),
 'hf-cashflow':('IFRS Foundation','IAS 7 Statement of Cash Flows','https://www.ifrs.org/issued-standards/list-of-standards/ias-7-statement-of-cash-flows/','',False),
 'hf-pension':('국민연금공단','국민연금 알아보기','https://www.nps.or.kr/pnsinfo/ntpsklg/getOHAF0097M0.do','',False),
}
SOURCE_TERMS={'근로계약서':'hf-contract','원천징수':'hf-withholding','원천징수의무자':'hf-withholding','국민연금':'hf-pension','기준소득월액':'hf-pension','현금흐름표':'hf-cashflow','영업활동현금흐름':'hf-cashflow','투자활동현금흐름':'hf-cashflow','재무활동현금흐름':'hf-cashflow','현금성자산':'hf-cashflow'}
GROUPS=[];NOTES={};ALIASES=[]
category=''
for line in Path(__file__).with_name('hr_finance.tsv').read_text().splitlines():
 if not line.strip():continue
 if line.startswith('# '):category=line[2:];continue
 term,aliases,definition,example=line.split('|')
 kind='현장 표현' if category=='인사·재무 현장 표현' else '전문 용어'
 GROUPS.append(('hrfinance',kind,category,SOURCE_TERMS.get(term,''),'|'.join([term,'',aliases.replace(',', ';'),definition,example,definition])))
 if category in ('근로관계·인사 운영','근태·휴가','급여·보상','사회보험·퇴직','세무·신고'):
  NOTES[term]='업무에서 쓰는 개념을 설명한 항목입니다. 실제 적용은 근로조건·계약·회계기준 및 해당 시점의 제도에 따라 확인합니다.'
