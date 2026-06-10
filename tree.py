import streamlit as st
import urllib.parse
import json

# --- 0-1. 팀 로고 이미지 URL 데이터베이스 (ESPN 공식 CDN) ---
TEAM_LOGOS = {
    "Buffalo Bills": "https://a.espncdn.com/i/teamlogos/nfl/500/buf.png",
    "Miami Dolphins": "https://a.espncdn.com/i/teamlogos/nfl/500/mia.png",
    "New England Patriots": "https://a.espncdn.com/i/teamlogos/nfl/500/ne.png",
    "New York Jets": "https://a.espncdn.com/i/teamlogos/nfl/500/nyj.png",
    "Baltimore Ravens": "https://a.espncdn.com/i/teamlogos/nfl/500/bal.png",
    "Cincinnati Bengals": "https://a.espncdn.com/i/teamlogos/nfl/500/cin.png",
    "Cleveland Browns": "https://a.espncdn.com/i/teamlogos/nfl/500/cle.png",
    "Pittsburgh Steelers": "https://a.espncdn.com/i/teamlogos/nfl/500/pit.png",
    "Houston Texans": "https://a.espncdn.com/i/teamlogos/nfl/500/hou.png",
    "Indianapolis Colts": "https://a.espncdn.com/i/teamlogos/nfl/500/ind.png",
    "Jacksonville Jaguars": "https://a.espncdn.com/i/teamlogos/nfl/500/jax.png",
    "Tennessee Titans": "https://a.espncdn.com/i/teamlogos/nfl/500/ten.png",
    "Denver Broncos": "https://a.espncdn.com/i/teamlogos/nfl/500/den.png",
    "Kansas City Chiefs": "https://a.espncdn.com/i/teamlogos/nfl/500/kc.png",
    "Las Vegas Raiders": "https://a.espncdn.com/i/teamlogos/nfl/500/lv.png",
    "Los Angeles Chargers": "https://a.espncdn.com/i/teamlogos/nfl/500/lac.png",
    "Dallas Cowboys": "https://a.espncdn.com/i/teamlogos/nfl/500/dal.png",
    "New York Giants": "https://a.espncdn.com/i/teamlogos/nfl/500/nyg.png",
    "Philadelphia Eagles": "https://a.espncdn.com/i/teamlogos/nfl/500/phi.png",
    "Washington Commanders": "https://a.espncdn.com/i/teamlogos/nfl/500/was.png",
    "Chicago Bears": "https://a.espncdn.com/i/teamlogos/nfl/500/chi.png",
    "Detroit Lions": "https://a.espncdn.com/i/teamlogos/nfl/500/det.png",
    "Green Bay Packers": "https://a.espncdn.com/i/teamlogos/nfl/500/gb.png",
    "Minnesota Vikings": "https://a.espncdn.com/i/teamlogos/nfl/500/min.png",
    "Atlanta Falcons": "https://a.espncdn.com/i/teamlogos/nfl/500/atl.png",
    "Carolina Panthers": "https://a.espncdn.com/i/teamlogos/nfl/500/car.png",
    "New Orleans Saints": "https://a.espncdn.com/i/teamlogos/nfl/500/no.png",
    "Tampa Bay Buccaneers": "https://a.espncdn.com/i/teamlogos/nfl/500/tb.png",
    "Arizona Cardinals": "https://a.espncdn.com/i/teamlogos/nfl/500/ari.png",
    "Los Angeles Rams": "https://a.espncdn.com/i/teamlogos/nfl/500/lar.png",
    "San Francisco 49ers": "https://a.espncdn.com/i/teamlogos/nfl/500/sf.png",
    "Seattle Seahawks": "https://a.espncdn.com/i/teamlogos/nfl/500/sea.png"
}

# --- 0-2. 코치 한줄 설명 데이터베이스 ---
COACH_SUMMARY = {
    # HC
    "Joe Brady": "팀 내 공격 코디네이터에서 내부 승진하여 지휘봉을 잡은 패스 전술가.",
    "Jeff Hafley": "그린베이 수비 코디네이터를 거쳐 마이애미의 새로운 수장으로 부임한 수비 전문 감독.",
    "Mike Vrabel": "테네시 감독직 이후 클리블랜드 컨설턴트를 거쳐 패트리어츠에 부임한 베테랑 감독.",
    "Aaron Glenn": "디트로이트의 수비 코디네이터로 성과를 낸 후 제츠의 감독으로 전격 발탁된 인물.",
    "Jesse Minter": "차저스의 수비 코디네이터를 거쳐 친정팀 볼티모어의 사령탑으로 복귀한 수비 전술가.",
    "Zac Taylor": "2019년부터 팀을 이끌며 패싱 공격 체제를 구축하고 강팀 반열에 올린 장기 집권 감독.",
    "Todd Monken": "레이븐스의 공격 코디네이터직을 거쳐 브라운스의 새로운 지휘봉을 잡은 공격 전술가.",
    "Mike McCarthy": "패커스와 카우보이스를 거쳐 전통의 피츠버그 수장으로 새로 부임한 베테랑 감독.",
    "DeMeco Ryans": "포티나이너스 수비 코디네이터 출신으로 친정팀 휴스턴의 리빌딩과 체질 개선을 이끈 감독.",
    "Shane Steichen": "이글스 공격 코디네이터 출신으로 젊은 쿼터백 중심의 유연한 공격 시스템을 운용하는 감독.",
    "Liam Coen": "램스와 버커니어스의 공격 코디네이터를 거쳐 잭슨빌의 신임 감독으로 부임한 인물.",
    "Robert Saleh": "제츠 감독을 거쳐 포티나이너스 수비 코디네이터 수복 후 테네시의 수장으로 새로 부임한 감독.",
    "Sean Payton": "뉴올리언스 왕조를 이끌었던 베테랑으로 현재 덴버의 전권을 쥐고 팀을 재건 중인 감독.",
    "Andy Reid": "이글스와 치프스에서 수많은 우승을 차지한 리그 역사상 최고의 공격 전술가이자 거장.",
    "Klint Kubiak": "시혹스의 공격 코디네이터로서 성과를 낸 후 레이더스의 신임 수장으로 전격 발탁된 인물.",
    "Jim Harbaugh": "대학 무대 우승 후 NFL로 복귀하여 차저스의 팀 체질 개선을 주도하고 있는 감독.",
    "Brian Schottenheimer": "팀 내 공격 코디네이터에서 오프시즌 기간 감독으로 전격 승진한 베테랑 전술가.",
    "John Harbaugh": "볼티모어 레이븐스에서 장기 집권하며 우승을 경험한 후 자이언츠로 새롭게 둥지를 튼 감독.",
    "Nick Sirianni": "콜츠 공격 코디네이터 출신으로 이글스를 강팀으로 유지하며 독특한 팀 문화를 구축한 감독.",
    "Dan Quinn": "시혹스 우승 DC와 애틀랜타 HC를 거쳐 워싱턴의 체질 개선을 지휘하고 있는 수비 전문 감독.",
    "Ben Johnson": "라이언스의 공격 코디네이터로서 리그 최정상급 공격진을 설계한 후 베어스의 신임 감독으로 부임한 전술가.",
    "Dan Campbell": "선수단 장악력과 강력한 리더십을 바탕으로 디트로이트를 만년 하위권에서 강팀으로 탈바꿈시킨 감독.",
    "Matt LaFleur": "램스와 타이탄스 OC를 거쳐 패커스에서 높은 승률과 안정적인 쿼터백 육성을 보여준 감독.",
    "Kevin O'Connell": "램스 공격 코디네이터 출신으로 바이킹스 부임 후 현대적이고 정교한 패싱 게임을 정착시킨 감독.",
    "Kevin Stefanski": "브라운스를 성공적으로 이끈 후 오프시즌에 애틀랜타의 새로운 사령탑으로 부임한 감독.",
    "Dave Canales": "시혹스와 버커니어스에서 전술적 역량을 입증한 후 팬서스의 젊은 피로 낙점된 감독.",
    "Kellen Moore": "카우보이스, 차저스, 이글스의 공격 코디네이터를 거쳐 세인츠의 수장으로 첫 발을 내딛은 인물.",
    "Todd Bowles": "수비 중심 팀 컬러를 유지하기 위해 감독직과 수비 플레이콜러 역할을 겸임하고 있는 인물.",
    "Mike LaFleur": "제츠와 램스의 공격 코디네이터를 거쳐 카디널스의 사령탑으로 전격 발탁된 젊은 전술가.",
    "Sean McVay": "현대 NFL의 공격 전술 트렌드를 선도하며 최연소 우승 기록을 세운 리그 최고 수준의 전술가.",
    "Kyle Shanahan": "현대 오펜스의 핵심인 와이드 존 스킴과 고유의 공격 시스템으로 팀을 리그 최강자로 유지 중인 거장.",
    "Mike Macdonald": "레이븐스의 수비 코디네이터로서 리그 최고 수준의 수비를 구축한 후 시혹스의 신임 감독으로 부임한 수비 전술가.",
    # OC
    "Pete Carmichael Jr.": "뉴올리언스에서 오랜 기간 드류 브리스와 숀 페이튼을 보좌했던 베테랑 패스 전술가.",
    "Bobby Slowik": "휴스턴의 플레이콜러를 거쳐 마이애미의 새로운 패스게임 시스템을 설계하러 합류한 인물.",
    "Josh McDaniels": "레이더스 감독직 이후 친정팀 뉴잉글랜드의 공격 지휘봉을 다시 잡은 플레이콜러.",
    "Frank Reich": "콜츠와 팬서스 감독 경력을 뒤로하고 제츠의 오펜스를 재건하기 위해 현장직으로 복귀한 베테랑.",
    "Declan Doyle": "시카고에서 영입된 30세의 젊은 전술가로 라마 잭슨 중심의 새 공격을 설계하는 인물.",
    "Dan Pitcher": "팀 내부에서 차근차근 승진하여 조 버로우와 잭 테일러 감독의 패싱 게임을 조율하는 코치.",
    "Travis Switzer": "볼티모어의 런게임 코디네이터 출신으로 브라운스의 지상 공격 강화를 위해 영입된 전술가.",
    "Brian Angelichio": "미네소타의 패스게임 코디네이터를 거쳐 마이크 매카시 사단의 공격을 지휘하는 인물.",
    "Nick Caley": "패트리어츠와 램스의 패스게임 코디네이터를 거쳐 휴스턴의 새로운 공격 수장으로 발탁된 인물.",
    "Jim Bob Cooter": "스타이컨 감독 체제하에서 쿼터백 육성과 공격 세부 전술 조율을 담당하는 베테랑 OC.",
    "Grant Udinski": "미네소타의 어시스턴트 OC 출신으로 잭슨빌의 젊은 공격진을 이끌기 위해 전격 영입된 코치.",
    "Brian Daboll": "자이언츠 감독직에서 물러난 후 로버트 살라 사단의 공격 전권을 쥐고 현장에 복귀한 인물.",
    "Davis Webb": "숀 페이튼 감독의 두터운 신임을 받아 31세의 나이로 덴버의 플레이콜러로 고속 승진한 인물.",
    "Eric Bieniemy": "시카고를 거쳐 친정팀 치프스로 복귀하여 앤디 리드 감독과 다시 호흡을 맞추는 베테랑.",
    "Andrew Janocko": "시애틀의 쿼터백 코치 출신으로 신임 클린트 쿠비악 감독과 함께 레이더스 공격을 이끄는 전술가.",
    "Mike McDaniel": "마이애미 감독직 이후 짐 하보 체제의 핵심 전술가이자 오펜스 설계자로 합류한 인물.",
    "Klayton Adams": "카디널스의 라인 코치 출신으로 브라이언 쇼텐하이머 감독 체제하에 공격 조율을 맡은 인물.",
    "Matt Nagy": "치프스에서 존 하보 사단으로 이동하여 자이언츠의 새로운 패싱 시스템을 책임지는 전술가.",
    "Sean Mannion": "그린베이 QB 코치 출신으로 닉 시리아니 감독 아래서 첫 플레이콜러 데뷔를 치르는 인물.",
    "David Blough": "팀 내 어시스턴트 QB 코치에서 공격 코디네이터로 전격 승진한 내부 인재.",
    "Press Taylor": "재규어스 OC를 거쳐 벤 존슨 신임 감독 체제의 시카고에서 패스게임을 조율하는 전술가.",
    "Drew Petzing": "애리조나의 오펜스를 이끌다 댄 캠벨 감독의 부름을 받고 라이온스에 합류한 전술가.",
    "Adam Stenavich": "맷 라플뢰르 감독 시스템 안에서 패커스의 안정적인 라인업과 런공격을 제어하는 OC.",
    "Wes Phillips": "케빈 오코넬 감독과 함께 바이킹스의 고효율 패싱 오펜스 세부 실행을 주도하는 코치.",
    "Tommy Rees": "클리블랜드에서 케빈 스테판스키 감독을 보좌하다 애틀랜타 사단으로 함께 이동한 OC.",
    "Brad Idzik": "데이브 카날레스 감독과 시혹스, 버커니어스 시절부터 긴밀하게 호흡을 맞춰온 최측근 전술가.",
    "Doug Nussmeier": "이글스 QB 코치 출신으로 켈렌 무어 신임 감독과 함께 세인츠의 패스 전술을 구축하러 온 인물.",
    "Zac Robinson": "램스와 애틀랜타를 거쳐 탬파베이의 플레이콜러로 새로 낙점된 맥베이 사단 출신 전술가.",
    "Nathaniel Hackett": "제츠를 거쳐 마이크 라플뢰르 신임 감독 체제의 카디널스 오펜스를 정비하기 위해 영입된 베테랑.",
    "Nathan Scheelhaase": "내부 승진을 통해 숀 맥베이 감독 아래에서 램스의 새로운 패스게임을 설계하게 된 코치.",
    "Klay Kubiak": "카일 섀너핸 감독 아래에서 단계별로 성장해 팀의 정식 공격 코디네이터 자리에 오른 인물.",
    "Brian Fleury": "포티나이너스의 런게임 코디네이터직을 수행한 후 시혹스에서 첫 플레이콜러 기회를 잡은 전술가.",
    # DC
    "Jim Leonhard": "덴버의 어시스턴트 HC를 거쳐 버팔로의 수비진을 3-4 포메이션 기반으로 개편하기 위해 부임한 전술가.",
    "Sean Duggan": "그린베이 라인배커 코치 출신으로 제프 하프리 신임 감독 체제의 마이애미 수비 전술을 보좌하는 인물.",
    "Zak Kuhr": "팀 내 라인배커 코치이자 인터림 DC를 거쳐 정식 수비 코디네이터로 보직이 승진된 내부 인사.",
    "Brian Duker": "라이온스와 마이애미의 세컨더리 코치를 거쳐 에런 글렌 신임 감독 사단의 수비 전술 조율하는 코치.",
    "Anthony Weaver": "마이애미 DC를 거쳐 제시 민터 신임 감독 체제의 레이븐스 프런트 세븐을 재건하러 합류한 베테랑.",
    "Al Golden": "팀 내 라인배커 코치에서 내부 승진하여 잭 테일러 감독 체제의 수비 전술 플레이콜을 전담하는 인물.",
    "Mike Rutenberg": "제츠와 애틀랜타의 패스게임 코디네이터를 거쳐 토드 몽켄 사단의 수비 수장으로 낙점된 인물.",
    "Patrick Graham": "자이언츠와 레이더스 DC를 거쳐 마이크 매카시 신임 감독 체제 피츠버그의 수비를 지휘하는 베테랑.",
    "Matt Burke": "디메코 라이언스 감독 시스템 안에서 휴스턴의 전방 압박과 디펜시브 라인 전술 실행을 조율하는 DC.",
    "Lou Anarumo": "벵갈스의 수비를 다년간 이끌다 셰인 스타이컨 감독 체제의 콜츠로 둥지를 튼 베테랑 전술가.",
    "Anthony Campanile": "패커스 런게임 코디네이터 출신으로 리암 코엔 신임 감독 체제 잭슨빌의 프런트 방어를 맡은 코치.",
    "Gus Bradley": "잭슨빌 HC와 콜츠 DC를 거쳐 로버트 살라 신임 감독 체제 테네시의 수비 시니어로 합류한 인물.",
    "Vance Joseph": "숀 페이튼 감독 체제하에서 덴버의 수비진을 굳건하게 제어하고 있는 베테랑 플레이콜러.",
    "Steve Spagnuolo": "다양한 블리츠 스킴으로 앤디 리드 감독과 함께 치프스 왕조의 수비 안방을 책임지는 거장 DC.",
    "Rob Leonard": "팀 내 디펜시브 라인 코치에서 내부 승진하여 클린트 쿠비악 신임 사단의 수비 전술을 총괄하는 인물.",
    "Chris O'Leary": "팀 내 세이프티 코치에서 짐 하보 감독의 선택을 받아 34세의 나이로 전격 발탁된 젊은 전술가.",
    "Christian Parker": "필라델피아 패스게임 코디네이터 출신으로 브라이언 쇼텐하이머 사단의 수비 재건을 맡은 34세 신성.",
    "Dennard Wilson": "타이탄스 DC를 거쳐 존 하보 신임 감독 체제 자이언츠의 백엔드 수비 전술을 정비하러 온 인물.",
    "Vic Fangio": "닉 시리아니 감독 아래에서 독자적인 가문형 수비 스킴을 고수하며 팀의 방어선을 통제하는 대부.",
    "Daronte Jones": "바이킹스 패스게임 코디네이터를 거쳐 댄 퀸 감독 체제 워싱턴의 2선 방어망을 설계하는 전술가.",
    "Dennis Allen": "세인츠 감독직 이후 벤 존슨 신임 감독 체제의 시카고 베어스 수비 전권을 쥐고 복귀한 베테랑.",
    "Kelvin Sheppard": "댄 캠벨 감독 체제하에서 라인배커 코치를 거쳐 내부 승진으로 수비 지휘봉을 잡은 인물.",
    "Jonathan Gannon": "카디널스 감독직 이후 맷 라플뢰르 감독 시스템의 수비 코디네이터로 현장에 복귀한 전술가.",
    "Brian Flores": "케빈 오코넬 감독 체제하에서 리그에서 가장 변칙적이고 공격적인 블리츠 시스템을 운용하는 DC.",
    "Jeff Ulbrich": "제츠의 DC를 거쳐 케빈 스테판스키 신임 감독 체제 애틀랜타의 수비 전술을 전담하게 된 인물.",
    "Ejiro Evero": "데이브 카날레스 감독의 신임 속에 팬서스의 3-4 베이스 수비 시스템 체계를 유지·통제하는 코치.",
    "Brandon Staley": "차저스 HC 경력 이후 켈렌 무어 신임 감독 체제 세인츠의 수비 조직력을 재정비하러 합류한 전술가.",
    "Nick Rallis": "마이크 라플뢰르 신임 감독 체제하에서도 카디널스의 젊은 수비진 전술 설계를 계속 전담하는 DC.",
    "Chris Shula": "숀 맥베이 감독 시스템 안에서 단계별 코치를 거쳐 내부 승진으로 램스 수비를 통제하는 코치.",
    "Raheem Morris": "애틀랜타 감독직 이후 카일 섀너핸 사단에 합류하여 포티나이너스의 수비진을 지휘하는 베테랑.",
    "Aden Durde": "마이크 맥도널드 감독의 수비 철학을 현장에서 구현하고 조율하는 시혹스의 수비 코디네이터."
}

# --- 0-3. 레전드 코치 생몰년도 ---
LEGEND_LIFESPANS = {
    "Pete Carroll": "1951 ~", "Mike Shanahan": "1952 ~", "Mike Holmgren": "1948 ~", "Bill Walsh": "1931 ~ 2007",
    "Tony Dungy": "1955 ~", "Bill Parcells": "1941 ~", "Bill Belichick": "1952 ~", "Marty Schottenheimer": "1943 ~ 2021",
    "Mike Zimmer": "1956 ~", "Bruce Arians": "1952 ~", "Jack Harbaugh": "1939 ~", "Bo Schembechler": "1929 ~ 2006",
    "Jason Garrett": "1966 ~", "Dirk Koetter": "1959 ~", "Gary Kubiak": "1961 ~", "Nick Saban": "1951 ~",
    "Jim Caldwell": "1955 ~", "Doug Pederson": "1968 ~", "Matt Eberflus": "1970 ~", "Doug Marrone": "1964 ~",
    "Vic Fangio": "1958 ~", "Dom Capers": "1950 ~", "Monte Kiffin": "1940 ~ 2024", "Jim Johnson": "1941 ~ 2009",
    "Wade Phillips": "1947 ~", "Bum Phillips": "1923 ~ 2013", "Jim Schwartz": "1966 ~", "Rex Ryan": "1962 ~",
    "Buddy Ryan": "1931 ~ 2016", "Kliff Kingsbury": "1979 ~", "Mike Leach": "1961 ~ 2022", "Hal Mumme": "1952 ~",
    "Earle Bruce": "1931 ~ 2018", "Ray Perkins": "1941 ~ 2020", "Sam Rutigliano": "1932 ~", "Bear Bryant": "1913 ~ 1983",
    "Woody Hayes": "1913 ~ 1987", "Jimmy Johnson": "1943 ~", "Marvin Lewis": "1958 ~", "Paul Brown": "1908 ~ 1991",
    "Chuck Noll": "1932 ~ 2014"
}

# --- 0-4. 15대 명문가 한줄 요약 데이터베이스 ---
MASTER_TREES = {
    "Paul Brown": "현대 NFL 오펜스의 근간이자 웨스트 코스트 및 존 블로킹 시스템의 절대적 뿌리",
    "Ray Perkins": "빌 파셀스와 빌 벨리칙, 션 페이튼으로 이어지는 강력한 수비 및 팀 재건의 제국",
    "Chuck Noll": "토니 던지와 프랭크 라이크를 거쳐 현대의 조직력 중심 명장들을 배출한 명문가",
    "Dom Capers": "빅 판지오를 중심으로 현대 NFL의 트렌디한 '투 하이 셸' 방어망을 구축한 수비 가문",
    "Earle Bruce": "피트 캐럴의 리더십을 거쳐 댄 퀸 등 선굵은 하이퍼 디펜시브 마인드를 낳은 계보",
    "Woody Hayes": "보 솀베클러와 하보 형제를 통해 대학과 프로 무대를 모두 정복한 피지컬 풋볼의 명가",
    "Sam Rutigliano": "마티 쇼텐하이머의 '마티볼' 철학을 기반으로 굵직한 공수 밸런스를 다진 계보",
    "Hal Mumme": "마이크 리치와 클리프 킹스베리로 이어지는 패싱 게임의 대혁명 '에어 레이드'의 고향",
    "Monte Kiffin": "리그의 패러다임을 바꾼 '탬파 2 수비' 전술을 집대성하고 전파한 정통 수비 가문",
    "Jimmy Johnson": "드래프트 가치 차트와 독창적인 선수단 빌딩 시스템으로 카우보이스 왕조를 이끈 파벌",
    "Bear Bryant": "브루스 아리안스와 토드 보울스로 이어지는 선굵은 다운필드 패싱 공격 사단",
    "Marvin Lewis": "역사적인 2000년대 레이븐스 명수비를 기반으로 토드 몽켄 등 정교한 전술가를 낳은 계보",
    "Bum Phillips": "웨이드 필립스와 밴스 조셉으로 이어지는 3-4 수비 스킴의 정통 계승자 가문",
    "Buddy Ryan": "NFL 역사상 가장 위력적인 압박 전술인 '46 디펜스'의 혈통을 잇는 독창적 수비 가문",
    "Jim Johnson": "창의적이고 맹렬한 블리츠 패키지로 치프스 왕조의 스파뇰로 등 변칙 수비 거장을 키워낸 안방"
}

# --- 1. 통합 데이터베이스 ---
RAW_DATA = """
Joe Brady,Sean Payton,Buffalo Bills,HC,2017–2018: 뉴올리언스 세인츠 (공격 어시스턴트) | 2020–2021: 캐롤라이나 팬서스 (OC) | 2022–2023: 버팔로 빌스 (QB 코치) | 2023–2025: 버팔로 빌스 (인터림 / 정식 OC)
Jeff Hafley,Matt LaFleur,Miami Dolphins,HC,2012–2013: 탬파베이 버커니어스 (공격 어시스턴트 / DB 코치) | 2014–2015: 클리블랜드 브라운스 (DB 코치) | 2016–2018: 샌프란시스코 포티나이너스 (DB 코치) | 2024–2025: 그린베이 패커스 (DC)
Mike Vrabel,Bill Belichick,New England Patriots,HC,2014–2016: 휴스턴 텍산스 (LB 코치) | 2017: 휴스턴 텍산스 (DC) | 2018–2023: 테네시 타이탄스 (HC) | 2024–2025: 클리블랜드 브라운스 (코칭 컨설턴트)
Aaron Glenn,Dan Campbell,New York Jets,HC,2014–2015: 클리블랜드 브라운스 (assistant DB 코치) | 2016–2020: 뉴올리언스 세인츠 (DB 코치) | 2021–2025: 디트로이트 라이온스 (DC)
Jesse Minter,Jim Harbaugh,Baltimore Ravens,HC,2017–2020: 볼티모어 레이븐스 (수비 어시스턴트 / DB 코치) | 2024–2025: 로스앤젤레스 차저스 (DC)
Zac Taylor,Sean McVay,Cincinnati Bengals,HC,2012–2015: 마이애미 돌핀스 (assistant QB 코치 / QB 코치 / 인터림 OC) | 2017–2018: 로스앤젤레스 램스 (어시스턴트 WR 코치 / QB 코치) | 2019–현재: 신시내티 벵갈스 (HC)
Todd Monken,Dirk Koetter,Cleveland Browns,HC,2002–2006: 잭슨빌 재규어스 (WR 코치) | 2016–2018: 탬파베이 버커니어스 (OC) | 2019: 클리블랜드 브라운스 (OC) | 2023–2025: 볼티모어 레이븐스 (OC)
Mike McCarthy,Marty Schottenheimer,Pittsburgh Steelers,HC,1999: 그린베이 패커스 (QB 코치) | 2000–2004: 뉴올리언스 세인츠 (OC) | 2005: 샌프란시스코 포티나이너스 (OC) | 2006–2018: 그린베이 패커스 (HC) | 2020–2025: 댈러스 카우보이스 (HC)
DeMeco Ryans,Kyle Shanahan,Houston Texans,HC,2017–2020: 샌프란시스코 포티나이너스 (수비 QC 코치 / LB 코치) | 2021–2022: 샌프란시스코 포티나이너스 (DC) | 2023–현재: 휴스턴 텍산스 (HC)
Shane Steichen,Nick Sirianni,Indianapolis Colts,HC,2014–2020: 로스앤젤레스 차저스 (공격 QC 코치 / QB 코치 / OC) | 2021–2022: 필라델피아 이글스 (OC) | 2023–현재: 인디애나폴리스 콜츠 (HC)
Liam Coen,Sean McVay,Jacksonville Jaguars,HC,2018–2020: 로스앤젤레스 램스 (assistant WR 코치 / assistant QB 코치) | 2022: 로스앤젤레스 램스 (OC) | 2024–2025: 탐파베이 버커니어스 (OC)
Robert Saleh,Kyle Shanahan,Tennessee Titans,HC,2005–2010: 휴스턴 텍산스 (수비 인턴 / 수비 QC 코치 / assistant LB 코치) | 2011–2013: 시애틀 시혹스 (수비 QC 코치) | 2014–2016: 잭슨빌 재규어스 (LB 코치) | 2017–2020: 샌프란시스코 포티나이너스 (DC) | 2021–2024: 뉴욕 제츠 (HC) | 2025: 샌프란시스코 포티나이너스 (DC)
Sean Payton,Bill Parcells,Denver Broncos,HC,1999–2002: 뉴욕 자이언츠 (QB 코치 / OC) | 2003–2005: 댈러스 카우보이스 (assistant HC / QB 코치) | 2006–2021: 뉴올리언스 세인츠 (HC) | 2023–현재: 덴버 브롱코스 (HC)
Andy Reid,Mike Holmgren,Kansas City Chiefs,HC,1992–1998: 그린베이 패커스 (OL 코치 / QB 코치) | 1999–2012: 필라델피아 이글스 (HC) | 2013–현재: 캔자스시티 치프스 (HC)
Klint Kubiak,Gary Kubiak,Las Vegas Raiders,HC,2016–2018: 덴버 브롱코스 (공격 QC 코치) | 2019–2021: 미네소타 바이킹스 (QB 코치 / OC) | 2022: 덴버 브롱코스 (패스게임 코디네이터 / QB 코치) | 2023–2024: 샌프란시스코 포티나이너스 (패스게임 코디네이터) | 2025: 시애틀 시혹스 (OC)
Jim Harbaugh,Jack Harbaugh,Los Angeles Chargers,HC,2002–2003: 오클랜드 레이더스 (공격 QC 코치) | 2011–2014: 샌프란시스코 포티나이너스 (HC) | 2024–현재: 로스앤젤레스 차저스 (HC)
Brian Schottenheimer,Marty Schottenheimer,Dallas Cowboys,HC,2006–2011: 뉴욕 제츠 (OC) | 2012–2014: 세인트루이스 램스 (OC) | 2016–2017: 인디애나폴리스 콜츠 (QB 코치) | 2018–2020: 시애틀 시혹스 (OC) | 2021: 잭슨빌 재규어스 (패스게임 코디네이터) | 2023–2025: 댈러스 카우보이스 (OC)
John Harbaugh,Andy Reid,New York Giants,HC,1998–2007: 필라델피아 이글스 (ST 코치 / DB 코치) | 2008–2025: 볼티모어 레이븐스 (HC)
Nick Sirianni,Frank Reich,Philadelphia Eagles,HC,2009–2012: 캔자스시티 치프스 (공격 QC 코치 / assistant WR 코치 / WR 코치) | 2013–2017: 샌디에이고/로스앤젤레스 차저스 (공격 QC 코치 / QB 코치 / WR 코치) | 2018–2020: 인디애나폴리스 콜츠 (OC) | 2021–현재: 필라델피아 이글스 (HC)
Dan Quinn,Pete Carroll,Washington Commanders,HC,2001–2006: 샌프란시스코, 마이애미 (DL 코치) | 2009–2010: 시애틀 시혹스 (DL 코치 / assistant HC) | 2013–2014: 시애틀 시혹스 (DC) | 2015–2020: 애틀랜타 팰컨스 (HC) | 2021–2023: 댈러스 카우보이스 (DC) | 2024–현재: 워싱턴 커맨더스 (HC)
Ben Johnson,Dan Campbell,Chicago Bears,HC,2012–2018: 마이애미 돌핀스 (공격 어시스턴트 / assistant WR 코치 / TE 코치 / WR 코치) | 2019–2025: 디트로이트 라이온스 (공격 QC 코치 / TE 코치 / OC)
Dan Campbell,Sean Payton,Detroit Lions,HC,2010–2015: 마이애미 돌핀스 (인턴 / TE 코치 / 인터림 HC) | 2016–2020: 뉴올리언스 세인츠 (assistant HC / TE 코치) | 2021–현재: 디트로이트 라이온스 (HC)
Matt LaFleur,Sean McVay,Green Bay Packers,HC,2008–2013: 휴스턴, 워싱턴 (공격 QC 코치 / QB 코치) | 2015–2016: 애틀랜타 팰컨스 (QB 코치) | 2017: 로스앤젤레스 램스 (OC) | 2018: 테네시 타이탄스 (OC) | 2019–현재: 그린베이 패커스 (HC)
Kevin O'Connell,Sean McVay,Minnesota Vikings,HC,2015: 클리블랜드 브라운스 (QB 코치) | 2016: 샌프란시스코 포티나이너스 (공격 특별 프로젝트) | 2017–2019: 워싱턴 레드스킨스 (QB 코치 / 패스게임 코디네이터 / OC) | 2020–2021: 로스앤젤레스 램스 (OC) | 2022–현재: 미네소타 바이킹스 (HC)
Kevin Stefanski,Mike Zimmer,Atlanta Falcons,HC,2006–2019: 미네소타 바이킹스 (assistant HC / assistant QB 코치 / TE 코치 / RB 코치 / QB 코치 / OC) | 2020–2025: 클리블랜드 브라운스 (HC)
Dave Canales,Pete Carroll,Carolina Panthers,HC,2010–2022: 시애틀 시혹스 (WR 코치 / QB 코치 / 패스게임 코디네이터) | 2023: 탬파베이 버커니어스 (OC) | 2024–현재: 캐롤라이나 팬서스 (HC)
Kellen Moore,Jason Garrett,New Orleans Saints,HC,2018–2022: 댈러스 카우보이스 (QB 코치 / OC) | 2023: 로스앤젤레스 차저스 (OC) | 2024–2025: 필라델피아 이글스 (OC)
Todd Bowles,Bruce Arians,Tampa Bay Buccaneers,HC,2000–2011: Jets, Browns, Cowboys, Dolphins (DB 코치 / assistant HC / 인터림 HC) | 2012: 필라델피아 이글스 (DB 코치 / 인터림 DC) | 2013–2014: 애리조나 카디널스 (DC) | 2015–2018: 뉴욕 제츠 (HC) | 2019–2021: 탬파베이 버커니어스 (DC) | 2022–현재: 탬파베이 버커니어스 (HC 겸 플레이콜러)
Mike LaFleur,Kyle Shanahan,Arizona Cardinals,HC,2014: 클리블랜드 브라운스 (공격 인턴) | 2015–2016: 애틀랜타 팰컨스 (공격 어시스턴트) | 2017–2020: 샌프란시스코 포티나이너스 (광역 패스게임 코디네이터) | 2021–2022: 뉴욕 제츠 (OC) | 2023–2025: 로스앤젤레스 램스 (OC)
Sean McVay,Mike Shanahan,Los Angeles Rams,HC,2008: 탬파베이 버커니어스 (공격 어시스턴트) | 2010–2016: 워싱턴 레드스킨스 (assistant TE 코치 / TE 코치 / OC) | 2017–현재: 로스앤젤레스 램스 (HC)
Kyle Shanahan,Mike Shanahan,San Francisco 49ers,HC,2004–2005: 탬파베이 버커니어스 (공격 QC 코치) | 2006–2009: 휴스턴 텍산스 (WR 코치 / QB 코치 / OC) | 2010–2013: 워싱턴 레드스킨스 (OC) | 2014: 클리블랜드 브라운스 (OC) | 2015–2016: 애틀랜타 팰컨스 (OC) | 2017–현재: 샌프란시스코 포티나이너스 (HC)
Mike Macdonald,John Harbaugh,Seattle Seahawks,HC,2014–2020: 볼티모어 레이븐스 (인턴 / 수비 QC 코치 / LB 코치 / DB 코치) | 2022–2023: 볼티모어 레이븐스 (DC) | 2024–현재: 시애틀 시혹스 (HC)
Pete Carmichael Jr.,Sean Payton,Buffalo Bills,OC,2006–2008: 뉴올리언스 세인츠 (QB 코치 / 패스게임 코디네이터) | 2009–2023: 뉴올리언스 세인츠 (OC) | 2024–2025: 덴버 브롱코스 (시니어 공격 어시스턴트)
Bobby Slowik,Kyle Shanahan,Miami Dolphins,OC,2011–2013: 워싱턴 레드스킨스 (수비 QC 코치) | 2019–2022: 샌프란시스코 포티나이너스 (공격 QC / 패스게임 어시스턴트 / 패스게임 코디네이터) | 2023–2024: 휴스턴 텍산스 (OC) | 2025: 마이애미 돌핀스 (시니어 패스게임 코디네이터)
Josh McDaniels,Bill Belichick,New England Patriots,OC,2005–2008: 뉴잉글랜드 패트리어츠 (QB 코치 / OC) | 2009–2010: 덴버 브롱코스 (HC) | 2011: 세인트루이스 램스 (OC / QB 코치) | 2012–2021: 뉴잉글랜드 패트리어츠 (OC / QB 코치) | 2022–2023: 라스베이거스 레이더스 (HC) | 2025–현재: 뉴잉글랜드 패트리어츠 (OC)
Frank Reich,Tony Dungy,New York Jets,OC,2012: 애리조나 카디널스 (WR 코치) | 2013–2015: 샌디에이고 차저스 (QB 코치 / OC) | 2016–2017: 필라델피아 이글스 (OC) | 2018–2022: 인디애나폴리스 콜츠 (HC) | 2023: 캐롤라이나 팬서스 (HC)
Declan Doyle,Matt Eberflus,Baltimore Ravens,OC,2019–2022: 뉴올리언스 세인츠 (공격 어시스턴트) | 2023–2024: 덴버 브롱코스 (TE 코치) | 2025: 시카고 베어스 (OC)
Dan Pitcher,Zac Taylor,Cincinnati Bengals,OC,2016–2019: 신시내티 벵갈스 (공격 QC 코치 / assistant QB 코치) | 2020–2023: 신시내티 벵갈스 (QB 코치) | 2024–현재: 신시내티 벵갈스 (OC)
Travis Switzer,John Harbaugh,Cleveland Browns,OC,2021–2023: 볼티모어 레이븐스 (공격 QC 코치 / assistant OL 코치) | 2024–2025: 볼티모어 레이븐스 (런게임 코디네이터)
Brian Angelichio,Kevin O'Connell,Pittsburgh Steelers,OC,2012–2021: Bucs, Browns, Packers, Redskins, Panthers (TE 코치) | 2022–2025: 미네소타 바이킹스 (TE 코치 / 패스게임 코디네이터)
Nick Caley,Bill Belichick,Houston Texans,OC,2015–2022: 뉴잉글랜드 패트리어츠 (공격 assistant / TE 코치) | 2023–2024: 로스앤젤레스 램스 (TE 코치 / 패스게임 코디네이터) | 2025–현재: 휴스턴 텍산스 (OC)
Jim Bob Cooter,Jim Caldwell,Indianapolis Colts,OC,2014–2018: 디트로이트 라이온스 (QB 코치 / OC) | 2019–2020: 뉴욕 제츠 (RB 코치) | 2021: 필라델피아 이글스 (코칭 컨설턴트) | 2022: 잭슨빌 재규어스 (패스게임 코디네이터) | 2023–현재: 인디애나폴리스 콜츠 (OC)
Grant Udinski,Matt Eberflus,Jacksonville Jaguars,OC,2023: 미네소타 바이킹스 (공격 assistant / assistant QB 코치) | 2024: 미네소타 바이킹스 (어시스턴트 OC / QB 코치) | 2025–현재: 잭슨빌 재규어스 (OC)
Brian Daboll,Nick Saban,Tennessee Titans,OC,2007–2012: Jets, Browns, Dolphins, Chiefs (OC) | 2013–2016: 뉴잉글랜드 패트리어츠 (TE 코치) | 2018–2021: 버팔로 빌스 (OC) | 2022–2025: 뉴욕 자이언츠 (HC)
Davis Webb,Brian Daboll,Denver Broncos,OC,2023: 버팔로 빌스 (공격 QB 코치) | 2024–2025: 덴버 브롱코스 (QB 코치 / 패스게임 코디네이터)
Eric Bieniemy,Andy Reid,Kansas City Chiefs,OC,2013–2017: 캔자스시티 치프스 (RB 코치) | 2018–2022: 캔자스시티 치프스 (OC) | 2023: 워싱턴 커맨더스 (assistant HC / OC) | 2024: UCLA (NCAA / 부감독 겸 OC) | 2025: 시카고 베어스 (RB 코치)
Andrew Janocko,Mike Zimmer,Las Vegas Raiders,OC,2015–2021: 미네소타 바이킹스 (공격 QC / OL 코치 / WR 코치 / QB 코치) | 2022–2023: 시카고 베어스 (QB 코치) | 2024–2025: 시애틀 시혹스 (QB 코치)
Mike McDaniel,Kyle Shanahan,Los Angeles Chargers,OC,2011–2016: Redskins, Browns, Falcons (WR 코치 / offensive assistant) | 2017–2021: 샌프란시스코 포티나이너스 (런게임 코디네이터 / OC) | 2022–2025: 마이애미 돌핀스 (HC)
Klayton Adams,Nick Sirianni,Dallas Cowboys,OC,2019–2020: 인디애나폴리스 콜츠 (assistant OL 코치) | 2021–2022: 인디애나폴리스 콜츠 (TE 코치) | 2023–2024: 애리조나 카디널스 (OL 코치) | 2025–현재: 댈러스 카우보이스 (OC)
Matt Nagy,Andy Reid,New York Giants,OC,2013–2017: 캔자스시티 치프스 (QB 코치 / OC) | 2018–2021: 시카고 베어스 (HC) | 2022–2025: 캔자스시티 치프스 (시니어 공격 어시스턴트 / QB 코치 / OC)
Sean Mannion,Sean McVay,Philadelphia Eagles,OC,2024: 시카고 베어스 (공격 assistant) | 2025: 그린베이 패커스 (QB 코치)
David Blough,Dan Quinn,Washington Commanders,OC,2024–2025: 워싱턴 커맨더스 (assistant QB 코치)
Press Taylor,Doug Pederson,Chicago Bears,OC,2013–2020: 필라델피아 이글스 (공격 QC / QB 코치 / 패스게임 코디네이터) | 2021: 인디애나폴리스 콜츠 (시니어 공격 어시스턴트) | 2022–2024: 잭슨빌 재규어스 (OC) | 2025: 시카고 베어스 (패스게임 코디네이터)
Drew Petzing,Kevin Stefanski,Detroit Lions,OC,2014–2019: 미네소타 바이킹스 (공격 assistant / WR 코치 / QB 코치) | 2020–2022: 클리블랜드 브라운스 (TE 코치 / QB 코치) | 2023–2025: 애리조나 카디널스 (OC)
Adam Stenavich,Matt LaFleur,Green Bay Packers,OC,2017–2018: 샌프란시스코 포티나이너스 (assistant OL 코치) | 2019–2021: 그린베이 패커스 (OL 코치 / 런게임 코디네이터) | 2022–현재: 그린베이 패커스 (OC)
Wes Phillips,Sean McVay,Minnesota Vikings,OC,2007–2018: Cowboys, Redskins (TE 코치 / assistant OL 코치) | 2019–2021: 로스앤젤레스 램스 (TE 코치 / 패스게임 코디네이터) | 2022–현재: 미네소타 바이킹스 (OC)
Tommy Rees,Nick Saban,Atlanta Falcons,OC,2016: 샌디에이고 차저스 (공격 QC 코치) | 2017–2023: Notre Dame, Alabama (NCAA / OC) | 2024: 클리블랜드 브라운스 (TE 코치 / 패스게임 패스재설계) | 2025: 클리블랜드 브라운스 (OC)
Brad Idzik,Dave Canales,Carolina Panthers,OC,2019–2022: 시애틀 시혹스 (공격 QC 코치 / assistant WR 코치) | 2023: 탬파베이 버커니어스 (WR 코치) | 2024–현재: 캐롤라이나 팬서스 (OC)
Doug Nussmeier,Jason Garrett,New Orleans Saints,OC,2018–2022: 댈러스 카우보이스 (TE 코치 / QB 코치) | 2023: 볼티모어 레이븐스 (QB 코치) | 2024: 필라델피아 이글스 (QB 코치) | 2025–현재: 뉴올리언스 세인츠 (OC)
Zac Robinson,Sean McVay,Tampa Bay Buccaneers,OC,2019–2023: 로스앤젤레스 램스 (공격 assistant / QB 코치 / 패스게임 코디네이터) | 2024–2025: 애틀랜타 팰컨스 (OC)
Nathaniel Hackett,Doug Marrone,Arizona Cardinals,OC,2013–2018: Bills, Jaguars (OC) | 2019–2021: 그린베이 패커스 (OC) | 2022: 덴버 브롱코스 (HC) | 2023–2024: 뉴욕 제츠 (OC) | 2025: 마이애미 돌핀스 (공격 수석 분석관)
Nathan Scheelhaase,Sean McVay,Los Angeles Rams,OC,2018–2023: Iowa State (NCAA / 런게임 코디네이터 / OC) | 2024: 로스앤젤레스 램스 (공격 어시스턴트) | 2025: 로스앤젤레스 램스 (패스게임 코디네이터)
Klay Kubiak,Gary Kubiak,San Francisco 49ers,OC,2021–2023: 샌프란시스코 포티나이너스 (수비 QC / assistant QB 코치) | 2024: 샌프란시스코 포티나이너스 (공격 패스게임 스페셜리스트) | 2025–현재: 샌프란시스코 포티나이너스 (OC)
Brian Fleury,Kyle Shanahan,Seattle Seahawks,OC,2016–2018: 마이애미 돌핀스 (풋볼 연구 분석관 / 가상 라인배커 코치) | 2020–2025: 샌프란시스코 포티나이너스 (공격 QC / TE 코치 / 런게임 코디네이터)
Jim Leonhard,Rex Ryan,Buffalo Bills,DC,2024: 덴버 브롱코스 (DB 코치) | 2025: 덴버 브롱코스 (assistant HC / 패스게임 코디네이터)
Sean Duggan,Matt LaFleur,Miami Dolphins,DC,2024–2025: 그린베이 패커스 (LB 코치)
Zak Kuhr,Bill Belichick,New England Patriots,DC,2020–2023: 뉴잉글랜드 패트리어츠 (수비 QC / 수비 assistant) | 2024–2025: 뉴잉글랜드 패트리어츠 (내부 LB 코치 / 인터림 DC)
Brian Duker,Vic Fangio,New York Jets,DC,2016–2023: Browns, 49ers, Lions (수비 assistant / DB 코치 / 세컨더리 코치) | 2024–2025: 마이애미 돌핀스 (세컨더리 코치 / 패스게임 코디네이터)
Anthony Weaver,John Harbaugh,Baltimore Ravens,DC,2016–2019: 휴스턴 텍산스 (DL 코치) | 2020: 휴스턴 텍산스 (DC / DL 코치) | 2021–2023: 볼티모어 레이븐스 (assistant HC / DL 코치) | 2024–2025: 마이애미 돌핀스 (DC)
Al Golden,Lou Anarumo,Cincinnati Bengals,DC,2016–2019: 디트로이트 라이온스 (TE 코치 / LB 코치) | 2020–2021: 신시내티 벵갈스 (LB 코치) | 2025–현재: 신시내티 벵갈스 (DC)
Mike Rutenberg,Raheem Morris,Cleveland Browns,DC,2020: 샌프란시스코 포티나이너스 (수비 패스게임 분석관) | 2021–2024: 뉴욕 제츠 (LB 코치) | 2025: 애틀랜타 팰컨스 (수비 패스게임 코디네이터)
Patrick Graham,Bill Belichick,Pittsburgh Steelers,DC,2019: 마이애미 돌핀스 (DC) | 2020–2021: 뉴욕 자이언츠 (assistant HC / DC) | 2022–2025: 라스베이거스 레이더스 (DC)
Matt Burke,Jim Schwartz,Houston Texans,DC,2017–2018: 마이애미 돌핀스 (DC) | 2019–2020: 필라델피아 이글스 (시니어 수비 어시스턴트 / 수비 패스게임 코디네이터) | 2021: 뉴욕 제츠 (게임 관리 특별 어시스턴트) | 2022: 애리조나 카디널스 (DL 코치) | 2023–현재: 휴스턴 텍산스 (DC)
Lou Anarumo,Zac Taylor,Indianapolis Colts,DC,2012–2017: 마이애미 돌핀스 (DB 코치 / 인터림 DC) | 2018: 뉴욕 자이언츠 (DB 코치) | 2019–2024: 신시내티 벵갈스 (DC) | 2025–현재: 인디애나폴리스 콜츠 (DC)
Anthony Campanile,Vic Fangio,Jacksonville Jaguars,DC,2020–2023: 마이애미 돌핀스 (LB 코치) | 2024: 그린베이 패커스 (LB 코치 / 런게임 코디네이터) | 2025–현재: 잭슨빌 재규어스 (DC)
Gus Bradley,Monte Kiffin,Tennessee Titans,DC,2013–2016: 잭슨빌 재규어스 (HC) | 2017–2020: 로스앤젤레스 차저스 (DC) | 2021: 라스베이거스 레이더스 (DC) | 2022–2024: 인디애나폴리스 콜츠 (DC) | 2025: 샌프란시스코 포티나이너스 (assistant HC)
Vance Joseph,Wade Phillips,Denver Broncos,DC,2016: 마이애미 돌핀스 (DC) | 2017–2018: 덴버 브롱코스 (HC) | 2019–2022: 애리조나 카디널스 (DC) | 2023–현재: 덴버 브롱코스 (DC)
Steve Spagnuolo,Jim Johnson,Kansas City Chiefs,DC,2007–2008: 뉴욕 자이언츠 (DC) | 2009–2011: 세인트루이스 램스 (HC) | 2012: 뉴올리언스 세인츠 (DC) | 2015–2017: 뉴욕 자이언츠 (DC / 인터림 HC) | 2019–현재: 캔자스시티 치프스 (DC)
Rob Leonard,Patrick Graham,Las Vegas Raiders,DC,2019–2021: 마이애미 돌핀스 (수비 assistant / OLB 코치) | 2022: 볼티모어 레이븐스 (OLB 코치) | 2023–2025: 라스베이거스 레이더스 (DL 코치 / 런게임 코디네이터)
Chris O'Leary,Jesse Minter,Los Angeles Chargers,DC,2024: 로스앤젤레스 차저스 (세이프티 코치)
Christian Parker,Vic Fangio,Dallas Cowboys,DC,2021–2023: 덴버 브롱코스 (DB 코치) | 2024–2025: 필라델피아 이글스 (DB 코치 / 패스게임 코디네이터)
Dennard Wilson,John Harbaugh,New York Giants,DC,2017–2022: Jets, Eagles (DB 코치 / 패스게임 코디네이터) | 2023: 볼티모어 레이븐스 (DB 코치) | 2024–2025: 테네시 타이탄스 (DC)
Vic Fangio,Dom Capers,Philadelphia Eagles,DC,2011–2014: 샌프란시스코 포티나이너스 (DC) | 2015–2018: 시카고 베어스 (DC) | 2019–2021: 덴버 브롱코스 (HC) | 2023: 마이애미 돌핀스 (DC) | 2024–현재: 필라델피아 이글스 (DC)
Daronte Jones,Mike Zimmer,Washington Commanders,DC,2018–2019: 신시내티 벵갈스 (DB 코치) | 2020: 미네소타 바이킹스 (DB 코치) | 2022–2025: 미네소타 바이킹스 (DB 코치 / 패스게임 코디네이터)
Dennis Allen,Sean Payton,Chicago Bears,DC,2011: 덴버 브롱코스 (DC) | 2012–2014: 오클랜드 레이더스 (HC) | 2015–2021: 뉴올리언스 세인츠 (시니어 수비 어시스턴트 / DC) | 2022–2024: 뉴올리언스 세인츠 (HC)
Kelvin Sheppard,Aaron Glenn,Detroit Lions,DC,2021: 디트로이트 라이온스 (수비 QC 코치) | 2022–현재: 디트로이트 라이온스 (LB 코치)
Jonathan Gannon,Matt Eberflus,Green Bay Packers,DC,2018–2020: 인디애나폴리스 콜츠 (DB 코치) | 2021–2022: 필라델피아 이글스 (DC) | 2023–2025: 애리조나 카디널스 (HC)
Brian Flores,Bill Belichick,Minnesota Vikings,DC,2011–2018: 뉴잉글랜드 패트리어츠 (수비 assistant / 세컨더리 / LB 코치 / 플레이콜러) | 2019–2021: 마이애미 돌핀스 (HC) | 2022: 피츠버그 스틸러스 (시니어 수비 어시스턴트 / LB 코치) | 2023–현재: 미네소타 바이킹스 (DC)
Jeff Ulbrich,Robert Saleh,Atlanta Falcons,DC,2015–2020: 애틀랜타 팰컨스 (LB 코치 / assistant HC / 인터림 DC) | 2021–2024: 뉴욕 제츠 (DC) | 2025–현재: 애틀랜타 팰컨스 (DC)
Ejiro Evero,Vic Fangio,Carolina Panthers,DC,2017–2021: 로스앤젤레스 램스 (세컨더리 코치 / 패스게임 코디네이터) | 2022: 덴버 브롱코스 (DC) | 2023–현재: 캐롤라이나 팬서스 (DC)
Brandon Staley,Vic Fangio,New Orleans Saints,DC,2020: 로스앤젤레스 램스 (DC) | 2021–2023: 로스앤젤레스 차저스 (HC) | 2024–2025: 샌프란시스코 포티나이너스 (assistant HC / 수비 부감독)
Nick Rallis,Jonathan Gannon,Arizona Cardinals,DC,2018–2020: 미네소타 바이킹스 (수비 QC / assistant LB 코치) | 2021–2022: 필라델피아 이글스 (LB 코치) | 2023–현재: 애리조나 카디널스 (DC)
Chris Shula,Sean McVay,Los Angeles Rams,DC,2017–2023: 로스앤젤레스 램스 (assistant LB / LB 코치 / DB 코치 / 패스러시 코디네이터) | 2024–현재: 로스앤젤레스 램스 (DC)
Raheem Morris,Monte Kiffin,San Francisco 49ers,DC,2009–2011: 탬파베이 버커니어스 (HC) | 2015–2020: 애틀랜타 팰컨스 (assistant HC / WR 코치 / DC / 인터림 HC) | 2021–2023: 로스앤젤레스 램스 (DC) | 2024–2025: 애틀랜타 팰컨스 (HC)
Aden Durde,Dan Quinn,Seattle Seahawks,DC,2018–2020: 애틀랜타 팰컨스 (수비 QC / OLB 코치) | 2021–2023: 댈러스 카우보이스 (DL 코치) | 2024–현재: 시애틀 시혹스 (DC)
Pete Carroll,Earle Bruce,None,Legend,USC 대학 왕조 건설 (NCAA 우승 2회) | 시애틀 시혹스 HC (슈퍼볼 XLVIII 우승) | NFL 역사상 가장 위대한 수비 '리전 오브 붐(Legion of Boom)' 창시자
Mike Shanahan,Bill Walsh,None,Legend,덴버 브롱코스 HC (슈퍼볼 XXXII, XXXIII 백투백 우승) | 현대 NFL 오펜스의 절대적 근간인 '존 블로킹(Zone Blocking)' 시스템의 대부
Mike Holmgren,Bill Walsh,None,Legend,그린베이 패커스 HC (슈퍼볼 XXXI 우승) | 시애틀 시혹스 HC (슈퍼볼 XL 진출) | 전설적인 쿼터백 브렛 파브의 은사
Bill Walsh,Paul Brown,None,Legend,샌프란시스코 49ers HC (슈퍼볼 3회 우승) | 짧고 정교한 타이밍 패스 위주의 '웨스트 코스트 오펜스(West Coast Offense)'를 창시한 NFL 최고의 전술 혁명가
Tony Dungy,Chuck Noll,None,Legend,탬파베이 버커니어스 HC | 인디애나폴리스 콜츠 HC (슈퍼볼 XLI 우승) | '탬파 2 수비'의 창시자이자 흑인 감독 최초 슈퍼볼 우승자
Bill Parcells,Ray Perkins,None,Legend,뉴욕 자이언츠 HC (슈퍼볼 XXI, XXV 우승) | 패트리어츠, 카우보이스 HC | '빅 튜나(Big Tuna)'라 불린 강력한 카리스마와 팀 리빌딩의 마술사
Bill Belichick,Bill Parcells,None,Legend,뉴잉글랜드 패트리어츠 HC (슈퍼볼 6회 우승) | 톰 브레이디와 함께 20년간 패트리어츠 왕조를 구축한 NFL 역대 최고(GOAT)의 명장
Marty Schottenheimer,Sam Rutigliano,None,Legend,브라운스, 치프스, 차저스 HC (정규시즌 200승) | 강력한 러싱 공격과 보수적인 수비를 중시하는 '마티볼(Martyball)' 철학의 아버지
Mike Zimmer,Bill Parcells,None,Legend,미네소타 바이킹스 HC | 댈러스 카우보이스 DC (슈퍼볼 XXX 우승) | 상대 QB를 혼란에 빠뜨리는 '더블 에이 갭 블리츠(Double A-Gap Blitz)'의 장인
Bruce Arians,Bear Bryant,None,Legend,탬파베이 버커니어스 HC (슈퍼볼 LV 우승) | 애리조나 카디널스 HC | "No risk it, no biscuit" 철학의 상남자 패싱 공격 전술가
Jack Harbaugh,Bo Schembechler,None,Legend,웨스턴 켄터키 대학 HC (NCAA Div I-AA 우승) | 존 하보(레이븐스 HC)와 짐 하보(차저스 HC) 형제를 길러낸 위대한 아버지
Bo Schembechler,Woody Hayes,None,Legend,미시간 대학 풋볼의 살아있는 전설 (빅텐 컨퍼런스 13회 우승) | 대학 풋볼 명예의 전당 헌액자
Jason Garrett,Jimmy Johnson,None,Legend,댈러스 카우보이스 HC (2010-2019) | 2016년 NFL 올해의 감독상 수상 | 선수 시절 카우보이스 백업 쿼터백으로 슈퍼볼 2회 우승
Dirk Koetter,Marvin Lewis,None,Legend,탬파베이 버커니어스 HC | 애틀랜타 팰컨스 OC | 타이트엔드와 수직 패싱 게임 활용에 특화된 오펜시브 마인드
Gary Kubiak,Mike Shanahan,None,Legend,덴버 브롱코스 HC (슈퍼볼 50 우승) | 휴스턴 텍산스 HC | 마이크 섀너핸의 수제자이자 존 블로킹 시스템의 정통 계승자
Nick Saban,Bill Belichick,None,Legend,앨라배마 대학 HC (내셔널 챔피언십 7회 우승) | 마이애미 돌핀스 HC | 대학 풋볼 역사상 가장 위대한 감독 (GOAT)
Jim Caldwell,Tony Dungy,None,Legend,인디애나폴리스 콜츠 HC (슈퍼볼 XLIV 진출) | 디트로이트 라이온스 HC | 페이튼 매닝의 전성기를 함께한 온화한 덕장
Doug Pederson,Andy Reid,None,Legend,필라델피아 이글스 HC (슈퍼볼 LII 우승) | 잭슨빌 재규어스 HC | '필리 스페셜(Philly Special)' 트릭 플레이 콜링의 주인공
Matt Eberflus,Frank Reich,None,Legend,시카고 베어스 HC | 인디애나폴리스 콜츠 DC | 탄탄하고 규율 잡힌 탬파 2 / 커버 2 시스템 기반의 디펜시브 마인드
Doug Marrone,Sean Payton,None,Legend,버팔로 빌스 HC | 잭슨빌 재규어스 HC (2017년 AFC 챔피언십 진출) | 강력한 오펜시브 라인(OL) 구축의 전문가
Vic Fangio,Dom Capers,None,Legend,덴버 브롱코스 HC | 49ers, 베어스, 돌핀스 DC | 현대 NFL 수비 트렌드인 '투 하이 셸(Two-High Shell)' 커버리지의 창시자
Dom Capers,None,None,Legend,캐롤라이나 팬서스, 휴스턴 텍산스 초대 HC | 그린베이 패커스 DC (슈퍼볼 XLV 우승) | 혁신적인 '존 블리츠(Zone Blitz)' 전술의 선구자
Monte Kiffin,None,None,Legend,탬파베이 버커니어스 DC (슈퍼볼 XXXVII 우승) | 토니 던지와 함께 커버 2 디펜스를 개량한 '탬파 2 수비'를 완성시킨 거장
Jim Johnson,None,None,Legend,필라델피아 이글스 전설의 DC (1999-2008) | 창의적이고 맹렬한 블리츠 패키지로 2000년대 리그 수비 트렌드를 지배한 인물
Wade Phillips,Bum Phillips,None,Legend,브롱코스, 빌스, 카우보이스 HC | 덴버 브롱코스 DC (슈퍼볼 50 우승) | 리그 역사상 최고의 1 갭(1-Gap) 3-4 디펜스 스페셜리스트
Bum Phillips,None,None,Legend,휴스턴 오일러스, 뉴올리언스 세인츠 HC | 웨이드 필립스의 아버지이자 카우보이 모자로 유명한 70년대의 낭만 명장
Jim Schwartz,Bill Belichick,None,Legend,디트로이트 라이온스 HC | 필라델피아 이글스 DC (슈퍼볼 LII 우승) | 공격적인 '와이드 9 (Wide-9)' 디펜시브 라인 배치의 대가
Rex Ryan,Buddy Ryan,None,Legend,뉴욕 제츠, 버팔로 빌스 HC | 볼티모어 레이븐스 DC (슈퍼볼 XXXV 우승) | 거침없는 입담과 변칙적인 블리츠 수비의 마스터
Buddy Ryan,None,None,Legend,필라델피아 이글스, 애리조나 카디널스 HC | 시카고 베어스 DC (슈퍼볼 XX 우승) | NFL 역사상 최강의 압박 수비인 '46 디펜스(46 Defense)'의 창조자
Kliff Kingsbury,Mike Leach,None,Legend,애리조나 카디널스 HC | 텍사스 테크 대학 HC | 패트릭 마홈스의 대학 시절 은사이자 에어 레이드 오펜스 신봉자
Mike Leach,Hal Mumme,None,Legend,워싱턴 스테이트, 미시시피 스테이트 HC | '에어 레이드(Air Raid)' 공격을 창안한 천재적이고 괴짜 같은 전술 혁명가
Hal Mumme,None,None,Legend,켄터키 대학 HC | 마이크 리치와 함께 대학 풋볼과 현대 NFL의 패싱 트렌드를 영원히 바꿔놓은 '에어 레이드' 시스템의 근원적 창시자
Earle Bruce,None,None,Legend,오하이오 스테이트 대학 HC | 빅텐(Big Ten) 챔피언십 4회 우승 | 어번 마이어, 피트 캐럴 등 수많은 명장들을 배출한 스승
Ray Perkins,None,None,Legend,뉴욕 자이언츠, 탬파베이 버커니어스 HC | 빌 파셀스와 빌 벨리칙이라는 역대급 명장들의 멘토 역할을 한 선구자
Sam Rutigliano,None,None,Legend,클리블랜드 브라운스 HC (1980년 NFL 올해의 감독상) | 마티 쇼텐하이머에게 브라운스 지휘봉을 물려준 멘토
Bear Bryant,None,None,Legend,앨라배마 대학 전설의 HC (내셔널 챔피언십 6회 우승) | 상징적인 하운드투스 모자로 기억되는 대학 풋볼의 거인
Woody Hayes,None,None,Legend,오하이오 스테이트 대학 전설의 HC (내셔널 챔피언십 5회 우승) | 보 솀베클러의 스승이자 터프한 런 게임의 대명사
Jimmy Johnson,None,None,Legend,댈러스 카우보이스 HC (슈퍼볼 XXVII, XXVIII 백투백 우승) | 현대 NFL의 필수 도구인 '드래프트 가치 차트(Draft Value Chart)'의 창시자
Marvin Lewis,None,None,Legend,신시내티 벵갈스 HC (2003-2018) | 볼티모어 레이븐스 DC (슈퍼볼 XXXV 우승) | 역대 최고로 꼽히는 2000년 레이븐스 수비를 지휘한 인물
Paul Brown,None,None,Legend,클리블랜드 브라운스, 신시내티 벵갈스 초대 HC (NFL 우승 3회) | 플레이콜링, 필름 분석, 마스크 등을 최초 도입한 NFL 오펜스의 근원적 아버지
Chuck Noll,None,None,Legend,피츠버그 스틸러스 HC (슈퍼볼 4회 우승) | 70년대 '스틸 커튼' 왕조를 구축하고 토니 던지를 지도한 위대한 명장
"""

# --- 2. 데이터 파싱 ---
@st.cache_data
def load_all_coaches():
    mentor_db = {}
    coach_db = {} 
    
    for line in RAW_DATA.strip().split('\n'):
        if not line.strip(): continue
        
        parts = line.strip().split(',', 4)
        if len(parts) == 5:
            coach, mentor, team, pos, career = [p.strip() for p in parts]
            clean_career = career.replace('"', '').replace("'", "")
            
            if coach not in mentor_db:
                mentor_db[coach] = None if mentor == "None" else mentor
            
            is_legend = (team == "None" and pos == "Legend")
            
            if coach not in coach_db:
                coach_db[coach] = {
                    "team": team if not is_legend else "",
                    "pos": [pos] if not is_legend else [],
                    "career": clean_career if not is_legend else "",
                    "legend_career": clean_career if is_legend else "",
                    "is_legend": is_legend,
                    "is_active": not is_legend
                }
            else:
                if is_legend:
                    coach_db[coach]["is_legend"] = True
                    coach_db[coach]["legend_career"] = clean_career
                else:
                    coach_db[coach]["is_active"] = True
                    coach_db[coach]["team"] = team
                    if pos not in coach_db[coach]["pos"]:
                        coach_db[coach]["pos"].append(pos)
                    coach_db[coach]["career"] = clean_career
                
    return mentor_db, coach_db

# --- 3. 핵심 엔진: 양방향 트리 추적 함수 ---
def get_mentors(coach_name, mentor_db):
    path = [coach_name]
    curr = coach_name
    while curr in mentor_db and mentor_db[curr] is not None:
        mentor = mentor_db[curr]
        path.append(mentor)
        curr = mentor
    return path

def get_disciples(coach_name, mentor_db):
    return [child for child, mentor in mentor_db.items() if mentor == coach_name]

# --- 4. D3.js 연동용 계층 JSON 동적 생성기 ---
def build_d3_hierarchy(node_name, mentor_db, coach_db):
    node_data = {"name": node_name}
    if node_name in coach_db:
        info = coach_db[node_name]
        node_data["is_active"] = info["is_active"]
        node_data["logo"] = TEAM_LOGOS.get(info["team"], "") if info["is_active"] else ""
        node_data["pos"] = ' / '.join(info['pos']) if isinstance(info['pos'], list) else info['pos']
    else:
        node_data["is_active"] = False
        node_data["logo"] = ""
        node_data["pos"] = ""
        
    children = [child for child, mentor in mentor_db.items() if mentor == node_name]
    if children:
        node_data["children"] = [build_d3_hierarchy(child, mentor_db, coach_db) for child in children]
    return node_data

# --- 5. 코치 이름용 클릭형 뱃지 생성기 ---
def create_coach_badge(c_name, coach_db):
    if c_name not in coach_db:
        return f'<span style="border-bottom: 2px dotted #9E9E9E; font-weight: bold; padding: 2px;">{c_name}</span>'
    
    c_info = coach_db[c_name]
    c_summary = COACH_SUMMARY.get(c_name)
    if not c_summary:
        if c_info["is_legend"]:
            lifespan = LEGEND_LIFESPANS.get(c_name, "생몰년도 정보 없음")
            c_summary = f"생몰년도: {lifespan}"
        else:
            c_summary = c_info["career"]
            
    c_summary = c_summary.replace(" | ", ", ").replace('"', '&quot;')
    
    color = "#1E88E5" if c_info["is_active"] else "#FF9800"
    link = f"/?coach={urllib.parse.quote(c_name)}"
    
    return f'<a href="{link}" target="_self" title="{c_summary}" style="cursor: pointer; border-bottom: 2px solid {color}; font-weight: bold; color: {color}; text-decoration: none; padding: 2px 4px;">{c_name}</a>'

# --- 6. UI 렌더링 ---
st.set_page_config(page_title="NFL Coaching Tree", layout="wide")

mentor_db, coach_db = load_all_coaches()

target_coach = st.query_params.get("coach")
default_mode_idx = 0
default_team_idx = 0
default_pos_idx = 0
default_legend_idx = 0

active_teams = sorted(list(set(i["team"] for i in coach_db.values() if i["is_active"])))
legend_list = sorted([name for name, i in coach_db.items() if i["is_legend"]])

# 링크 셋팅
if target_coach in coach_db:
    info = coach_db[target_coach]
    if info["is_active"]:
        default_mode_idx = 0
        if info["team"] in active_teams:
            default_team_idx = active_teams.index(info["team"])
        if info["pos"]:
            first_pos = info["pos"][0]
            if first_pos in ["HC", "OC", "DC"]:
                default_pos_idx = ["HC", "OC", "DC"].index(first_pos)
    else:
        default_mode_idx = 1
        if target_coach in legend_list:
            default_legend_idx = legend_list.index(target_coach)

st.sidebar.title("🏈 NFL 코칭 트리")
mode = st.sidebar.radio("🔍 조회 모드", ["🛡️ NFL 현역 스태프", "🌟 레전드 명예의 전당"], index=default_mode_idx)

is_viewing_legend = (mode == "🌟 레전드 명예의 전당")
selected_coach = None

if not is_viewing_legend:
    sel_team = st.sidebar.selectbox("1. 팀을 선택하세요", active_teams, index=default_team_idx)
    sel_pos = st.sidebar.radio("2. 직책을 선택하세요", ["HC", "OC", "DC"], index=default_pos_idx)
    selected_coach = next((name for name, i in coach_db.items() if i["is_active"] and i["team"] == sel_team and sel_pos in i["pos"]), None)
else:
    selected_coach = st.sidebar.selectbox("전설적인 명장", legend_list, index=default_legend_idx)

if selected_coach:
    st.query_params.coach = selected_coach

if selected_coach:
    info = coach_db[selected_coach]
    
    if is_viewing_legend:
        st.title(f"🌟 {selected_coach} (Legend)")
        st.caption("은퇴/명예의 전당 | Legend")
        career_info = info["legend_career"]
    else:
        team_logo_url = TEAM_LOGOS.get(info["team"], "")
        st.markdown(
            f"""
            <div style="display: flex; align-items: center; gap: 15px; margin-bottom: 10px;">
                <img src="{team_logo_url}" width="60" style="object-fit: contain;">
                <h1 style="margin: 0; padding: 0;">{selected_coach}</h1>
            </div>
            """, 
            unsafe_allow_html=True
        )
        display_pos = ' / '.join(info['pos'])
        st.caption(f"{info['team']} | {display_pos}")
        career_info = info["career"]
    
    summary = COACH_SUMMARY.get(selected_coach)
    if not summary:
        if is_viewing_legend or not info["is_active"]:
            lifespan = LEGEND_LIFESPANS.get(selected_coach, "생년 정보 없음")
            summary = f"🗓️ 생몰년도: {lifespan}"
        else:
            summary = "이 코치에 대한 간단한 한줄평이 아직 등록되지 않았습니다."
            
    st.markdown(f"> **💡 {summary}**")
    st.divider()
        
    st.subheader("🌳 코칭 트리 (가르침을 받은 계보)")
    mentors_path = get_mentors(selected_coach, mentor_db)
    mentor_html = " <span style='color: #4CAF50;'>⬅</span> ".join([create_coach_badge(c, coach_db) for c in mentors_path])
    st.markdown(
        f'<div style="padding: 1rem; border-radius: 0.5rem; background-color: rgba(76, 175, 80, 0.1); border: 1px solid rgba(76, 175, 80, 0.4); margin-bottom: 1.5rem; line-height: 2;">{mentor_html}</div>', 
        unsafe_allow_html=True
    )
    
    st.subheader("🌱 파생 코칭 트리 (가르침을 준 제자)")
    disciples = get_disciples(selected_coach, mentor_db)
    if disciples:
        disciple_html = " &nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp; ".join([create_coach_badge(d, coach_db) for d in disciples])
        st.markdown(
            f'<div style="padding: 1rem; border-radius: 0.5rem; background-color: rgba(33, 150, 243, 0.1); border: 1px solid rgba(33, 150, 243, 0.4); margin-bottom: 1.5rem; line-height: 2;">{disciple_html}</div>', 
            unsafe_allow_html=True
        )
    else:
        st.info("아직 이 코치로부터 파생된 현역 감독/코디네이터 데이터가 없습니다.")
    
    st.subheader("📜 주요 경력")
    if career_info:
        with st.container(border=True):
            for item in [i.strip() for i in career_info.split('|') if i.strip()]:
                st.markdown(f"🔹 **{item}**")
    else:
        st.warning("등록된 경력 정보가 없습니다.")
else:
    st.warning("선택하신 조건에 해당하는 데이터가 없습니다.")

# =====================================================================
# 🎯 7. 15대 명문가 마스터 익스플로러 엔진 (접이식)
# =====================================================================
st.markdown("---")
st.header("📊 NFL 15대 명문가 마스터 트리 익스플로러 (접이식)")

master_roots = sorted(list(MASTER_TREES.keys()))

root_mentor = mentors_path[-1] if selected_coach and mentors_path else None
default_master_idx = 0
if root_mentor in master_roots:
    default_master_idx = master_roots.index(root_mentor)

selected_master = st.selectbox(
    "조회할 명문 가문을 선택하세요", 
    master_roots, 
    index=default_master_idx, 
    format_func=lambda x: f"👑 {x} 가문"
)

st.markdown(f"> **💡 가문 특징:** *{MASTER_TREES[selected_master]}*")

hierarchy_data = build_d3_hierarchy(selected_master, mentor_db, coach_db)
json_data_str = json.dumps(hierarchy_data)

# 💡 목표 인물로 트리를 자동 펼침(Auto-Expand)하기 위해 파이썬 변수 전달
target_coach_js = selected_coach if selected_coach else ""

html_template = """
<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <script src="https://d3js.org/d3.v7.min.js"></script>
    <style>
        body { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; margin: 0; background-color: #ffffff; overflow: hidden; }
        .node { cursor: default; }
        .node circle { fill: #fff; stroke: #FF9800; stroke-width: 2.5px; cursor: pointer; }
        .node image { cursor: pointer; }
        .node text { font-size: 13px; font-weight: bold; fill: #333333; cursor: pointer; }
        .node text:hover { text-decoration: underline; fill: #d32f2f !important; }
        .link { fill: none; stroke: #e0e0e0; stroke-width: 2px; }
        #canvas { width: 100%; height: 580px; cursor: grab; }
        #canvas:active { cursor: grabbing; }
    </style>
</head>
<body>
    <div id="canvas"></div>
    <script>
        const rawData = __JSON_DATA_HERE__;
        const targetCoachName = "__TARGET_COACH_NAME__";
        
        const margin = {top: 20, right: 120, bottom: 20, left: 120},
              width = window.innerWidth,
              height = 580;

        let i = 0, duration = 600, root;

        const svg = d3.select("#canvas").append("svg")
            .attr("width", "100%")
            .attr("height", height)
            .call(d3.zoom().on("zoom", function (event) {
                svgGroup.attr("transform", event.transform);
            }))
            .append("g");

        const svgGroup = svg.append("g")
            .attr("transform", "translate(" + margin.left + "," + (height/2 - 20) + ")");

        const treemap = d3.tree().nodeSize([45, 220]);

        root = d3.hierarchy(rawData, d => d.children);
        root.x0 = 0;
        root.y0 = 0;

        // 💡 [핵심] 자동 펼침 로직 (선택된 코치 경로만 열어두고 나머진 접기)
        function collapseAll(d) {
            if (d.children) {
                d._children = d.children;
                d._children.forEach(collapseAll);
                d.children = null;
            }
        }

        function containsTarget(d, target) {
            if (d.data.name === target) return true;
            let found = false;
            if (d.children) {
                d.children.forEach(child => { if(containsTarget(child, target)) found = true; });
            }
            if (d._children) {
                d._children.forEach(child => { if(containsTarget(child, target)) found = true; });
            }
            return found;
        }

        function expandPathToTarget(d, target) {
            if (containsTarget(d, target)) {
                if (d._children) {
                    d.children = d._children;
                    d._children = null;
                }
                if (d.children) {
                    d.children.forEach(child => expandPathToTarget(child, target));
                }
            } else {
                collapseAll(d);
            }
        }

        if (root.children) {
            if (targetCoachName && targetCoachName !== "") {
                root.children.forEach(child => expandPathToTarget(child, targetCoachName));
            } else {
                root.children.forEach(collapseAll);
            }
        }

        update(root);

        function update(source) {
            const treeData = treemap(root);
            const nodes = treeData.descendants(),
                  links = treeData.links();

            nodes.forEach(d => d.y = d.depth * 230);

            const node = svgGroup.selectAll('g.node')
                .data(nodes, d => d.id || (d.id = ++i));

            const nodeEnter = node.enter().append('g')
                .attr('class', 'node')
                .attr('transform', d => `translate(${source.y0},${source.x0})`);

            // 아이콘(로고/원형) 클릭 시 트리 폴더 열고 접기
            nodeEnter.each(function(d) {
                const g = d3.select(this);
                let element;
                // 💡 [핵심] 트리가 열렸을 때 현역이면 로고 이미지를 삽입!
                if (d.data.is_active && d.data.logo) {
                    element = g.append('image')
                     .attr('href', d.data.logo)
                     .attr('x', -14)
                     .attr('y', -14)
                     .attr('width', 28)
                     .attr('height', 28)
                     .style('filter', 'drop-shadow(0px 2px 4px rgba(0,0,0,0.15))');
                } else {
                    element = g.append('circle')
                     .attr('r', 7)
                     .style("fill", d => d._children ? "#FF9800" : "#fff");
                }

                element.on('click', function(event, d) {
                    event.stopPropagation();
                    if (d.children) {
                        d._children = d.children;
                        d.children = null;
                    } else {
                        d.children = d._children;
                        d._children = null;
                    }
                    update(d);
                });
            });

            // 텍스트 클릭 시 프로필 페이지로 연동
            nodeEnter.append('text')
                .attr('dy', '.35em')
                .attr('x', d => d.children || d._children ? -18 : 18)
                .attr('text-anchor', d => d.children || d._children ? 'end' : 'start')
                .text(d => {
                    let display = d.data.name;
                    if(d.data.pos) display += ' (' + d.data.pos + ')';
                    return display;
                })
                .style('fill', d => d.data.is_active ? '#1E88E5' : '#FF9800')
                .on('click', function(event, d) {
                    event.stopPropagation(); 
                    window.parent.location.search = '?coach=' + encodeURIComponent(d.data.name);
                });

            const nodeUpdate = nodeEnter.merge(node);

            nodeUpdate.transition()
                .duration(duration)
                .attr('transform', d => `translate(${d.y},${d.x})`);

            nodeUpdate.select('circle')
                .attr('r', 7)
                .style("fill", d => d._children ? "#FF9800" : "#fff");

            const nodeExit = node.exit().transition()
                .duration(duration)
                .attr('transform', d => `translate(${source.y},${source.x})`)
                .remove();

            nodeExit.select('circle').attr('r', 1e-6);
            nodeExit.select('image').attr('width', 1e-6).attr('height', 1e-6);
            nodeExit.select('text').style('fill-opacity', 1e-6);

            const link = svgGroup.selectAll('path.link')
                .data(links, d => d.target.id);

            const linkEnter = link.enter().insert('path', "g")
                .attr('class', 'link')
                .attr('d', d => {
                    const o = {x: source.x0, y: source.y0};
                    return diagonal(o, o);
                });

            const linkUpdate = linkEnter.merge(link);

            linkUpdate.transition()
                .duration(duration)
                .attr('d', d => diagonal(d.source, d.target));

            link.exit().transition()
                .duration(duration)
                .attr('d', d => {
                    const o = {x: source.x, y: source.y};
                    return diagonal(o, o);
                })
                .remove();

            nodes.forEach(d => {
                d.x0 = d.x;
                d.y0 = d.y;
            });

            function diagonal(s, d) {
                return `M ${s.y} ${s.x}
                        C ${ (s.y + d.y) / 2 } ${s.x},
                          ${ (s.y + d.y) / 2 } ${d.x},
                          ${d.y} ${d.x}`;
            }
        }
    </script>
</body>
</html>
"""

d3_collapsible_html = html_template.replace("__JSON_DATA_HERE__", json_data_str).replace("__TARGET_COACH_NAME__", target_coach_js)

st.components.v1.html(d3_collapsible_html, height=580)
