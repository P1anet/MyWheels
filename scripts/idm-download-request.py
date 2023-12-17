import subprocess
__idm_location_shell = r"""for /f "tokens=1,2,* " %i in ('REG QUERY HKEY_CURRENT_USER\Software\DownloadManager /v ExePath ^| find /i "ExePath"') do @echo %k"""
__down_root_path__shell = r"""echo %USERPROFILE%\Downloads"""
IDM = str(subprocess.check_output(__idm_location_shell, shell=True)).replace('b\'', '').replace('\\r\\n\'', '')
down_root_path = str(subprocess.check_output(__down_root_path__shell, shell=True)).replace('b\'', '').replace('\\r\\n\'', '').replace('\\\\', '\\')
subprocess.call(IDM)

down_url = r"""http://qdall01.baidupcs.com/file/f7bbed66ap5120403aca54cc122659c8?bkt=en-06f5c65000af0ed6471501ab6290fcb72d2fa37a53fa578c0b8118caa7602f0da461b09930e75ba7&fid=2015768268-778750-448687715273001&time=1678865899&sign=FDTAXUbGERLQlBHSKfWaqir-DCb740ccc5511e5e8fedcff06b081203-UQkeOkmZMTwYWibZzjs5TG3ourQ%3D&to=d0,34&size=3075145702&sta_dx=3075145702&sta_cs=0&sta_ft=zip&sta_ct=7&sta_mt=0&fm2=MH%2CYangquan%2CAnywhere%2C%2C%E6%B5%99%E6%B1%9F%2Cct&ctime=1641408457&mtime=1678865635&resv0=-1&resv1=0&resv2=rlim&resv3=5&resv4=3075145702&vuk=2015768268&iv=0&htype=&randtype=em&tkbind_id=0&newver=1&newfm=1&secfm=1&flow_ver=3&pkey=en-c04d1c4f879a512837e47b11e5c63175b80bf56e88475444bb6badf8911451d53a70857dc7a25dce&sl=76480590&expires=8h&rt=pr&r=190718219&mlogid=1708188921576957903&vbdid=2917091859&fin=%E7%A1%AC%E6%A0%B8%E7%9A%84%E6%99%B6%E6%99%B6%E9%85%B1%E7%9A%84lut%E5%8C%85%E6%94%B6%E8%97%8F.zip&bflag=34-34&rtype=1&devuid=O%7Cd41d8cd98f00b204e9800998ecf8427e&dp-logid=1708188921576957903&dp-callid=0.1.1&tsl=80&csl=80&fsl=-1&csign=wZgfLUVzmh9vdATalCmvnwhlwiA%3D&so=1&ut=6&uter=0&serv=0&uc=1069429310&ti=974fa6b90eb1b435d3050bce67c73474a2bf26236d787c89305a5e1275657320&hflag=30&from_type=3&adg=c_5edced12070e4f47c77fb4802ad23530&reqlabel=778750_l_6df2c43191c7080b07e0ced02743023f_-1_adb987dbf7a58593e6e93ef1c071408a&ibp=1&by=themis&filename=%E7%A1%AC%E6%A0%B8%E7%9A%84%E6%99%B6%E6%99%B6%E9%85%B1%E7%9A%84lut%E5%8C%85%E6%94%B6%E8%97%8F.zip"""
down_path = down_root_path + r"""\硬核的晶晶酱的lut包收藏.zip"""
output_filename = r"""硬核的晶晶酱的lut包收藏.zip"""
subprocess.call([IDM, '/d',down_url, '/p',down_path, '/f', output_filename, '/n', '/a', '/s'])
      
  