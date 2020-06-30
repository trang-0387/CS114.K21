trans={'một':1, 'hai':2,'đôi':2, 'ba':3, 'bốn':4, 'tư':4, 'năm':5, 'sáu':6, 'bảy':7, 'tám':8, 'chín':9,'kg':'kg','ki-lô-gam':'kg','mét':'m','m':'m','một':'mỗi'}
def prepro(debai):
  if 'tiền' in debai: debai=debai.replace('tiền','đồng')
  sentences=debai.split('.')
  words=[]
  for sentence in sentences:
    words.append(sentence.split(' '))
  digits=[]
  for i in debai.split(' '):
    if i.isdigit():
      digits.append(int(i))
  return sentences,words,digits

def cong(words,digits):
  donvi=words[-1][words[-1].index('nhiêu')+1]
  pheptoan=f'{digits[0]} + {digits[1]} = {digits[0]+digits[1]} ({donvi})'
  return pheptoan,digits[0]+digits[1],donvi

def tru(words,digits):
  digits.sort()
  donvi=words[-1][words[-1].index('nhiêu')+1]
  pheptoan=f'{digits[1]} - {digits[0]} = {digits[1]-digits[0]} ({donvi})'
  return pheptoan,digits[1]-digits[0],donvi

def nhan(words,digits):
  donvi=words[-1][words[-1].index('nhiêu')+1]
  pheptoan=f'{digits[0]} x {digits[1]} = {digits[0]*digits[1]} ({donvi})'
  return pheptoan,digits[0]*digits[1],donvi

def chia(words,digits,key_word=None):
  digits.sort()
  if key_word==None: donvi=words[-1][words[-1].index('nhiêu')+1]
  else: donvi=words[0][words[0].index(key_word)]
  pheptoan=f'{digits[1]} : {digits[0]} = {digits[1]//digits[0]} ({donvi})'
  return pheptoan,digits[1]//digits[0],donvi

def tim_phep_toan(gia_thiet,sentences,digits,words):
  k=0
  for word in sentences[-1].lower().split():
    if word.isdigit(): k=1
  
  if (k==1): 
    #Trường hợp câu hỏi có số (1 lời giải)
    donvi=[]
    gt=list(gia_thiet.lower().split(' '))    # Phân tích giả thiết thành các từ

    for i in gt:
      if (i in trans.keys()): gt[gt.index(i)]=trans[i]                                                                                                                                # Đổi các đơn vị và một thành mỗi
    if ('mỗi' in gt): donvi.append(gt[gt.index('mỗi')+1])                                                                                                                   # Tìm đơn vị sau từ mỗi

    for i in words[-1]:      
      if i.isdigit(): donvi.append(words[-1][words[-1].index(i)+1])                                                                                                     # Tìm đơn vị phía sau số của câu hỏi
    if donvi[0]==donvi[1]: return 3                                                                                                                                                   #Nếu đơn vị sau từ mỗi và đơn vị sau số của câu hỏi trùng nhau thì là nhân
    else: return 4                                                                                                                                                                               # và khác nhau thì chia
  elif ('mỗi' in sentences[-1].lower()) or ('một' in sentences[-1].lower()): return 4                                                                           #Trường hợp: Có mỗi bên trong câu hỏi => chia
  elif ('tất cả' in sentences[-1].lower()) or (('cả hai' in sentences[-1].lower())):                                                                                # TRường hợp: tất cả và cả hai ở câu hỏi
    donvi,gt=[],gia_thiet.split()                                                                                                                                                          # gt là giả thiết sau khi tách thành các từ
    for word in gt:
      if word.isdigit():
        donvi.append(gt[gt.index(word)+1])                                                                                                                                      #Lấy 2 đơn vị sau 2 con số của giải thiết
    if donvi[0]==donvi[1]: return 1                                                                                                                                                   #Nếu 2 đơn vị trùng nhau thì cộng
    else: return 3                                                                                                                                                                               # ngược lại thì nhân
  elif ('còn lại' in sentences[-1].lower()): return 2                                                                                                                            #Trường hợp còn lại ở câu hỏi => trừ
  elif ('mỗi' in gia_thiet.lower()) :                                                                                                                                                     #Trường hợp có từ mỗi trong giả thiết
    if ('đều' in gia_thiet.lower()): return 4                                                                                                                                         #Và trong giả thiết có từ đều (chia đều, thưởng đều, cho đều...) => chia
    else:
      donvi=[]
      gt=list(gia_thiet.lower().split())
      donvi.append(gt[gt.index('mỗi')+1]) if ('mỗi' in gia_thiet.lower()) else donvi.append(gt[gt.index('một')+1])                        #Lấy đơn vị sau từ mỗi và nếu không có mỗi thì lấy đơn vị sau từ một
      donvi.append(words[-1][words[-1].index('nhiêu')+1])                                                                                                            #Lấy đơn vị sau chữ bao nhiêu
      if (donvi[0]==donvi[1]): return 4                                                                                                                                             #Nếu hai đơn vị trùng nhau thì chia
      else: return 3                                                                                                                                                                            #ngược lại thì nhân
  elif ('một phần' in gia_thiet.lower()) or ('/' in gia_thiet):                                                                                                              #Trường hợp: câu giả thiết có / hoặc một phần
    if ('một phần' in gia_thiet.lower()):                                                                                                                                            #Trường hợp từ một phần trong giả thiết
      gt=list(gia_thiet.split(' '))
      digits.append(trans[gt[gt.index('phần')+1]])                                                                                                                           #Đổi chữ sau chữ phần thành con số tương ứng và đưa vào digits
    else: 
      digits.append(int(gia_thiet[gia_thiet.find('/')+1]))                                                                                                                   #Nếu trong giải thiết là / thì lấy con số sau / append vào digits
    for j in gia_thiet: 
      if j.isdigit(): break                                                                                                                                                                    # Tìm con số đầu tiên trong giả thiết
    if ('và' in gia_thiet[gia_thiet.find(j):].lower()): return 3                                                                                                              #Nếu trong giả thiết có 'và' nằm phía sau của con số đầu tiên thì nhân
    else: return 4                                                                                                                                                                             #ngược lại thì chia
  elif ('lần' in gia_thiet.lower()):                                                                                                                                                      #Trường hợp: có từ lần trong giả thiết
    gt=list(gia_thiet.split())
    so=gt[gt.index('lần')-1]                                                                                                                                                             #Lấy ký tự phía sau chữ lần
    if so.isdigit()==False: digits.append(trans[so])                                                                                                                         #Nếu ký tự phía sau không phải là số thì chuyển sang số và append vào digits
    for t in gia_thiet:
      if t.isdigit(): break
    if 'và' in gia_thiet[gia_thiet.find(t):]: return 4
    if ('gấp' in gia_thiet.lower()) or ('nhiều hơn' in gia_thiet.lower()) or ('nhiều gấp' in gia_thiet.lower())  :return 3               
    else: return 4
  elif ('ít hơn' in gia_thiet.lower()): return 2
  else: return 1                                                                                                                                                                                            

def Rut_ve_don_vi(sentences,words,digits):
  pheptoan=[]
  if ',' in sentences[0]: sentences[0]=sentences[0][sentences[0].find(',')+2:]
  if ',' in words[0]: words[0]=words[0][words[0].index(',')+1:]
  dv=[]
  for word in words:
    for i in word:
      if i.isdigit(): dv.append([i,word[word.index(i)+1]])
  digits_new=digits[:2].copy()
  digits_new.sort()
  for i in sentences[0]:
    if i.isdigit(): 
      id=sentences[0].find(i)
      break
  loigiai1=sentences[0][id:].replace(str(digits_new[1]),'số').replace(str(digits_new[0]),'một')
  kw=words[0][words[0].index(str(digits_new[1]))+1]
  pt,kq,donvi=chia(words,digits_new,key_word=kw)
  pheptoan.append(pt)
  if int(dv[0][0])>int(dv[1][0]): m=0 
  else: m=1
  digits_new=[digits[2],kq]
  if dv[2][1]==dv[m][1]: pt,kq,donvi=chia(words,digits_new)
  else: pt,kq,donvi=nhan(words,digits_new)
  pheptoan.append(pt)
  return pheptoan,loigiai1,kq,donvi

def giai(sentences,words,digits):
  gia_thiet,loigiai,pheptoan='',[],[]
  for sentence in sentences[:-1]:
    gia_thiet+=sentence
  loigiai.append(sentences[-1][5:].replace('bao nhiêu','số')+' là:')

  nhan_biet_gt=['một phần','hơn','/','gấp']
  nhan_biet_ch=['một phần','hơn','/','gấp','tất cả','cả hai','còn lại','và']
  k=0
  for j in nhan_biet_gt:
    if j in gia_thiet: k+=1
  for j in nhan_biet_ch:
    if j in sentences[-1]: k+=1
  
  if (len(digits)==3):
    kind=2
    pheptoan,loigiai1,kq,donvi=Rut_ve_don_vi(sentences,words,digits)
    loigiai.append(loigiai1)
  elif k>=2:
    kind=2
    gia_thiet=gia_thiet.replace(',','.')
    if ('nhiều hơn' in gia_thiet) or ('ít hơn' in gia_thiet):
      ok='nhiều hơn' in gia_thiet
      for j in gia_thiet.split('.')[-1].split():
        if j.isdigit(): break
      start=gia_thiet.split('.')[-1].find('nhiều hơn') if ok else gia_thiet.split('.')[-1].find('ít hơn')
      end=gia_thiet.split('.')[-1].find(j)
      drop=gia_thiet.split('.')[-1][start:end+len(j)] 
      loi_giai_1=gia_thiet.split('.')[-1].replace(drop,'số')+' là:'
      loigiai.append(loi_giai_1)
      pre_kq=digits[0]+digits[1] if ok else digits[0]-digits[1]
      change={True:'+',False:'-'}
      phep_toan_1=f'{digits[0]} {change[ok]} {digits[1]} = {pre_kq} ({words[-2][words[-2].index(j)+1]})' 
      pheptoan.append(phep_toan_1)
      ok2='còn lại' in gia_thiet
      kq=pre_kq+digits[0] if ok2==False else digits[0]-pre_kq
      donvi=sentences[-1][sentences[-1].find('nhiêu')+5:]
      phep_toan_2=f'{digits[0]} {change[not ok2]} {pre_kq} = {kq} ({donvi})'
      pheptoan.append(phep_toan_2)
    else: 
      gia_thiet=''
      for sentence in sentences[:-1]:
        gia_thiet+=sentence+'.'
      gia_thiet=gia_thiet.replace(',','.')
      kind=3
      if '/' in gia_thiet.lower(): 
        gia_thiet=gia_thiet.replace('1/','một phần ')
      ok='một phần' in gia_thiet
      index_so=gia_thiet.split().index('phần')+1 if ok else gia_thiet.split().index('gấp')+1
      so=gia_thiet.split()[index_so]
      if gia_thiet.split()[index_so].isdigit()==False: 
        gia_thiet.replace(so,str(trans[so]))
        digits.append(int(trans[so])) 
      print(ok)
      loi_giai_1=gia_thiet.split('.')[-2].replace('một phần ','&') if ok else gia_thiet.split('.')[-2]  #Do có một ký tự None sau cùng
      print(loi_giai_1)
      loi_giai_1=((loi_giai_1[:loi_giai_1.find('bằng' )]+'là:' if 'bằng' in gia_thiet else loi_giai_1[:loi_giai_1.find('&' )]+loi_giai_1[loi_giai_1.find('&')+2:]+' là:') if ok else loi_giai_1[:loi_giai_1.find('gấp')]+'là:') 
      #if '&' not in loi_giai_1 else (loi_giai_1[:loi_giai_1.find('&')]+loi_giai_1[loi_giai_1.find('&')+2:]+'là:'
      loigiai.append(loi_giai_1)
      change={True:':' ,False:'x'}
      change2={True:'-',False:'+'}
      if len(digits)<2:     digits.append(int(gia_thiet.split()[gia_thiet.split().index('phần')+1]))
      pre_kq=digits[0]//digits[1] if ok else digits[0]*digits[1]
      dv=sentences[-1][sentences[-1].find('nhiêu')+5:]       #Xem lại đơn vị
      phep_toan_1=f'{digits[0]} {change[ok]} {digits[1]} = {pre_kq} ({dv})'
      pheptoan.append(phep_toan_1)
      ok2='còn lại' in sentences[-1]
      print(ok2)
      kq=pre_kq+digits[0] if not ok2 else digits[0]-pre_kq
      donvi=dv
      phep_toan_2=f'{digits[0]} {change2[ok2]} {pre_kq} = {kq} ({donvi})'
      pheptoan.append(phep_toan_2)
  else:
     #1:cộng  2: trừ   3:nhân   4:chia
    flat=0
    flat=tim_phep_toan(gia_thiet,sentences,digits,words)
    kind=1
    if (flat==1): pheptoan1,kq,donvi=cong(words,digits)
    elif (flat==2): pheptoan1,kq,donvi=tru(words,digits)
    elif (flat==3): pheptoan1,kq,donvi=nhan(words,digits)
    elif (flat==4):  pheptoan1,kq,donvi=chia(words,digits)
    pheptoan.append(pheptoan1)
  
  dapso=f'Đáp số: {kq} {donvi}'
  return kind,loigiai,pheptoan,dapso

def xuli_loigiai(lg):
    lg=lg.strip()
    lg=lg[0].upper()+lg[1:]
    return lg

def Solve(debai):
    debai=debai[:-1]
    if 'mấy' in debai: debai=debai.replace('mấy','bao nhiêu')
    sentences,words,digits=prepro(debai)
    kind,loigiai,pheptoan,dapso=giai(sentences,words,digits)
    new_loigiai=[]
    for loigiai_ in loigiai:
        new_loigiai.append(xuli_loigiai(loigiai_))   
    if kind==1:
        result=new_loigiai[0]+'\n'+pheptoan[0]+'\n'+dapso
    else:
      result=new_loigiai[1]+'\n'+pheptoan[0]+'\n'+new_loigiai[0]+'\n'+pheptoan[1]+'\n'+dapso
    return result.strip()
#print(Solve(input()))
