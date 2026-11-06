LINK='https://steamcommunity.com/sharedfiles/filedetails/?id=3828956017'
COPY={'english': ('Darkest Refined — 20-Hero Complete Edition | Hero Rebalance', '20-hero complete edition (DLC heroes included)', 'This item changes only this hero. For all 20 heroes, subscribe to the complete edition linked above instead. It requires the DLC listed on its page. Do not enable the complete edition together with this item or the original Rebalance.'), 'koreana': ('다키스트 리파인드 — 20영웅 통합판 | 영웅 리밸런스', '20영웅 통합판 · DLC 영웅 포함', '이 항목은 해당 영웅만 변경합니다. 20영웅 전체를 변경하려면 위 통합판을 대신 구독하세요. 통합판 페이지에 표시된 DLC가 필요합니다. 통합판과 이 개별판 또는 기존 리밸런스를 동시에 활성화하지 마세요.'), 'schinese': ('Darkest Refined — 20英雄整合版 | 英雄再平衡', '20英雄整合版（包含DLC英雄）', '此项目只修改这一名英雄。若要修改全部20名英雄，请改为订阅上方整合版。整合版需要其页面列出的DLC。请勿将整合版与此单独版或原Rebalance同时启用。'), 'tchinese': ('Darkest Refined — 20英雄整合版 | 英雄再平衡', '20英雄整合版（包含DLC英雄）', '此項目只修改這一名英雄。若要修改全部20名英雄，請改為訂閱上方整合版。整合版需要其頁面列出的DLC。請勿將整合版與此單獨版或原Rebalance同時啟用。'), 'brazilian': ('Darkest Refined — Edição completa: 20 heróis | Rebalanceamento', 'Edição completa com 20 heróis (inclui heróis de DLC)', 'Este item modifica apenas este herói. Para modificar todos os 20, assine a edição completa acima em vez deste item. Ela exige os DLCs listados em sua página. Não ative a edição completa junto com este item ou o Rebalance original.'), 'french': ('Darkest Refined — Édition complète : 20 héros | Rééquilibrage', 'Édition complète : 20 héros, héros de DLC inclus', 'Cet élément ne modifie que ce héros. Pour les 20 héros, abonnez-vous plutôt à l’édition complète ci-dessus. Elle nécessite les DLC indiqués sur sa page. N’activez pas l’édition complète avec cet élément ou le Rebalance original.'), 'german': ('Darkest Refined — Komplettpaket: 20 Helden | Helden-Rebalance', 'Komplettpaket mit 20 Helden (inklusive DLC-Helden)', 'Dieses Paket verändert nur diesen Helden. Für alle 20 Helden abonniere stattdessen das oben verlinkte Komplettpaket. Es benötigt die auf seiner Seite aufgeführten DLCs. Aktiviere es nicht zusammen mit diesem Einzelpaket oder dem ursprünglichen Rebalance.'), 'polish': ('Darkest Refined — Pełny pakiet: 20 bohaterów | Rebalans', 'Pełny pakiet 20 bohaterów (w tym bohaterowie z DLC)', 'Ten element zmienia tylko tego bohatera. Aby zmienić wszystkich 20, zasubskrybuj zamiast niego pełny pakiet z powyższego linku. Wymaga on DLC wymienionych na jego stronie. Nie włączaj pełnego pakietu razem z tym elementem ani z oryginalnym Rebalance.'), 'russian': ('Darkest Refined — Все 20 героев | Ребаланс', 'Полный набор: 20 героев, включая героев DLC', 'Этот мод изменяет только одного героя. Для всех 20 героев подпишитесь вместо него на полный набор по ссылке выше. Ему нужны DLC, указанные на его странице. Не включайте полный набор вместе с этим модом или исходным Rebalance.'), 'spanish': ('Darkest Refined — Edición completa: 20 héroes | Reequilibrio', 'Edición completa de 20 héroes (incluye héroes de DLC)', 'Este elemento solo modifica a este héroe. Para modificar a los 20, suscríbete en su lugar a la edición completa del enlace anterior. Requiere los DLC indicados en su página. No actives la edición completa junto con este elemento ni con el Rebalance original.')}
def banner(lang):
 _,head,body=COPY[lang]
 return f'[h2][url={LINK}]{head}[/url][/h2]\n{body}\n\n'

# WS-NAV-002: enforce approved navigation at the shared upload boundary.
STANDALONES = {3832933701,3832933671,3832933678,3832933691,3832933684}
def preserve_navigation(item_id, language, title, description, current):
 if language not in COPY or (title is None and description is None):
  return title, description
 if item_id not in STANDALONES and item_id != 3828956017:
  return title, description
 title = current['title'] if title is None else title
 description = current['description'] if description is None else description
 if item_id == 3828956017:
  title = COPY[language][0]
 else:
  prefix = banner(language)
  if not description.startswith(prefix):
   description = prefix + description
 return title, description
