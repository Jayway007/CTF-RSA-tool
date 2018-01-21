# coding:utf-8
import requests
from bs4 import BeautifulSoup
import gmpy2
import libnum


def solve(N):
    return factordb(N)


# factordb.com
def factordb(N):
    res = requests.get('http://factordb.com/index.php?query=' + str(N))
    soup = BeautifulSoup(res.text, 'lxml')
    factor = []
    for i in soup.find_all('font'):
        if i.string and '.' not in str(i.string) and '*' not in str(i.string):
            factor.append(int(i.string))
    while N in factor:
        factor.remove(N)
    if factor:
        return factor
    else:
        print '----------factor N fail----------'
        print 'can not factor N or it is a prime number:' + str(N)
        print 'you may try tool "yafu" or other attck method'
        print '---------------------------------'
        return


# 模不互素: 需要（n1，e1，c1）及（n2，e2），且e1 == e2。解密c1
def gcd_n1_n2_no_1(n1, n2, e, c1):
    p1 = gmpy2.gcd(n1, n2)
    q1 = n1 / p1
    d = gmpy2.invert(e, (p1 - 1) * (q1 - 1))
    plain = gmpy2.powmod(c1, d, n1)
    plain = hex(plain)[2:]
    if len(plain) % 2 != 0:
        plain = '0' + plain
    print plain.decode('hex')


# 共模攻击: 需要（n1，e1，c1）及（n2，e2, c2），且n1 == n2 and gcd(e1,e2) == 1。
def one_n_2_e(N, e1, e2, c1, c2):
    gcd, s, t = gmpy2.gcdext(e1, e2)
    if s < 0:
        s = -s
        c1 = gmpy2.invert(c1, N)
    if t < 0:
        t = -t
        c2 = gmpy2.invert(c2, N)
    plain = gmpy2.powmod(c1, s, N) * gmpy2.powmod(c2, t, N) % N
    print libnum.n2s(plain)


def isqrt(n):
    x = n
    y = (x + n // x) // 2
    while y < x:
        x = y
        y = (x + n // x) // 2
    return x


# |p-q|较小
def p_q_2_close(n):
    a = isqrt(n)
    b2 = a * a - n
    b = isqrt(n)
    count = 0
    while b * b != b2:
        a = a + 1
        b2 = a * a - n
        b = isqrt(b2)
        count += 1
    p = a + b
    q = a - b
    assert n == p * q
    return p, q


if __name__ == '__main__':
    print 'test factordb'
    print solve(23)
    print solve(87924348264132406875276140514499937145050893665602592992418171647042491658461)
    # SCTF rsa2
    print 'test 模不互素'
    n1 = 20823369114556260762913588844471869725762985812215987993867783630051420241057912385055482788016327978468318067078233844052599750813155644341123314882762057524098732961382833215291266591824632392867716174967906544356144072051132659339140155889569810885013851467056048003672165059640408394953573072431523556848077958005971533618912219793914524077919058591586451716113637770245067687598931071827344740936982776112986104051191922613616045102859044234789636058568396611030966639561922036712001911238552391625658741659644888069244729729297927279384318252191421446283531524990762609975988147922688946591302181753813360518031
    n2 = 19083821613736429958432024980074405375408953269276839696319265596855426189256865650651460460079819368923576109723079906759410116999053050999183058013281152153221170931725172009360565530214701693693990313074253430870625982998637645030077199119183041314493288940590060575521928665131467548955951797198132001987298869492894105525970519287000775477095816742582753228905458466705932162641076343490086247969277673809512472546919489077884464190676638450684714880196854445469562733561723325588433285405495368807600668761929378526978417102735864613562148766250350460118131749533517869691858933617013731291337496943174343464943
    e = 65537
    c1 = 0x68d5702b70d18238f9d4a3ac355b2a8934328250efd4efda39a4d750d80818e6fe228ba3af471b27cc529a4b0bef70a2598b80dd251b15952e6a6849d366633ed7bb716ed63c6febd4cd0621b0c4ebfe5235de03d4ee016448de1afbbe61144845b580eed8be8127a8d92b37f9ef670b3cdd5af613c76f58ca1a9f6f03f1bc11addba30b61bb191efe0015e971b8f78375faa257a60b355050f6435d94b49eab07075f40cb20bb8723d02f5998d5538e8dafc80cc58643c91f6c0868a7a7bf3bf6a9b4b6e79e0a80e89d430f0c049e1db4883c50db066a709b89d74038c34764aac286c36907b392bc299ab8288f9d7e372868954a92cdbf634678f7294096c7
    gcd_n1_n2_no_1(n1, n2, e, c1)
    # Jarvis OJ very hard RSA
    print 'test 共模攻击'
    N = 0x00b0bee5e3e9e5a7e8d00b493355c618fc8c7d7d03b82e409951c182f398dee3104580e7ba70d383ae5311475656e8a964d380cb157f48c951adfa65db0b122ca40e42fa709189b719a4f0d746e2f6069baf11cebd650f14b93c977352fd13b1eea6d6e1da775502abff89d3a8b3615fd0db49b88a976bc20568489284e181f6f11e270891c8ef80017bad238e363039a458470f1749101bc29949d3a4f4038d463938851579c7525a69984f15b5667f34209b70eb261136947fa123e549dfff00601883afd936fe411e006e4e93d1a00b0fea541bbfc8c5186cb6220503a94b2413110d640c77ea54ba3220fc8f4cc6ce77151e29b3e06578c478bd1bebe04589ef9a197f6f806db8b3ecd826cad24f5324ccdec6e8fead2c2150068602c8dcdc59402ccac9424b790048ccdd9327068095efa010b7f196c74ba8c37b128f9e1411751633f78b7b9e56f71f77a1b4daad3fc54b5e7ef935d9a72fb176759765522b4bbc02e314d5c06b64d5054b7b096c601236e6ccf45b5e611c805d335dbab0c35d226cc208d8ce4736ba39a0354426fae006c7fe52d5267dcfb9c3884f51fddfdf4a9794bcfe0e1557113749e6c8ef421dba263aff68739ce00ed80fd0022ef92d3488f76deb62bdef7bea6026f22a1d25aa2a92d124414a8021fe0c174b9803e6bb5fad75e186a946a17280770f1243f4387446ccceb2222a965cc30b3929L
    e1 = 17
    e2 = 65537
    c1 = libnum.s2n('cbOLM8rQ87801yasrDeDbsFbFZ+3AeemK30qzl4F8/ijwyRY1p7nqwTCK0yuCGa5ZMIWSeu2uVfQrur6z51q/N+N8chki/Oet1KeHMBb6Q6k2b8UyugfY4QlmJB1deRE7D9w76zAn51wFIHZ2w3eci9JwpWbCH83AS/tP5k5HbczaV705RAuckpA6sDcFHDZI7WGQdH33bEYbJiqFX8Ra7tS/T80OTXy5H6lpYYJBoy+M7G5WuzHRaSCDM5niis2qgOakyXPlpRbxvFpWRz/bzpUvsjfGzQXKdqUibx2lfPa9BpIiMern656dTp494kVIsyVK4gP7U0cQAQk8xL0gBz+9Kfrrzq/Xi+yS+ab7WkDaUw7papLgeBkAKL7stL5U4MlF27RDxe3svGjxdhTVxJngcuXlISpOs8sXSDaIgVaT/yOF0NjBG2R4B/LXHtMOETBSUotlk5mnVnrKm7NGPdZFN50jKGCIzyNak2nx+dhGi+1qcC6JrKOb16urdpLssxfQacWxtEENmK19FMF6+yoU6MDU0fWWWGz0IN1LWkstvFIv2nuqkr1hqf9kJBzN3xRJOUabY44hAWU71rj9kl6Kp7Aasxj5mXJbnaAHponHFl+JjcBiqNB758yG5v4HshDRPvLBAu3BdS3E/5gB+MKiBburlYRELlc2hymQYE='.decode('base64'))
    c2 = libnum.s2n('MAaKGD0WNcewbAfaGKCjmjMpjHNOPttsVag90jtiDNBSrV3AGQxcmY12CT02MhAZjVWQLyhfdNSw7sxuKWqG7z1PJSWlEo6cGg0HphDGUnXV0F3OvjqhmJEfHtMzYRhbLNe2q6oqylEplPNM8Cmvkb6n9k1IadQskK2YPCTWeHDlpF7Tf0X8TcJGRXUvOE6ShlQSfR8fg4gxpC3E33aviKiLrLaUWyLEZ2TAMdMy/qI9j9mtu7ojlHWe9P2+/GCid8Rl/BGQv9KV91b/jAlrbzUYtrc6e9wCoSuKQ7uliUjT7WKBW/HF5R1RuCI/FTLs1Cbfx2m82yBzhv4thRXxrbNV/g+pbQaFaXPIC9PAjPN3k5HnsHoxYW3lMAnpvb1naTrhWZ9rS67fNwxFHy1cf2eCqSv5EFJKtURRIOfNcXMxzjMlNjDD3KO7qTCLoVRrR3z6sXEDukNQ5aQPKBL9PzA7UhjJyiXOZKpR5/LQJqyCeE+GDnI3NJNWx9wjpBn+DiFez9JN1a5eWda2jKFxAHiR+WMvOw0HWDj6KVQKTzroQu7XypIPM2MwlamrSJYQoBMaEBOtTSzPAKim+xlDo5Kkiat1B89lr/oxtNsUhRrgEV+RGfT7/LZYfeju+7iG3cEGyVv2l+HZ3z2viZ/WepQpIu55rlz0H+5C9Q5Tfmc='.decode('base64'))
    one_n_2_e(N, e1, e2, c1, c2)
    print 'test |p-q|较小'
    n = 966808932627497190635859236054960349099463975227350564265384373280336699853387254070662881265937565163000758606154308757944030571837175048514574473061401566330836334647176655282619268592560172726526643074499534129878217409046045533656897050117438496357231575999185527675071002803951800635220029015932007465117818739948903750200830856115668691007706836952244842719419452946259275251773298338162389930518838272704908887016474007051397194588396039111216708866214614779627566959335170676055025850932631053641576566165694121420546081043285806783239296799795655191121966377590175780618944910532816988143056757054052679968538901460893571204904394975714081055455240523895653305315517745729334114549756695334171142876080477105070409544777981602152762154610738540163796164295222810243309051503090866674634440359226192530724635477051576515179864461174911975667162597286769079380660782647952944808596310476973939156187472076952935728249061137481887589103973591082872988641958270285169650803792395556363304056290077801453980822097583574309682935697260204862756923865556397686696854239564541407185709940107806536773160263764483443859425726953142964148216209968437587044617613518058779287167853349364533716458676066734216877566181514607693882375533
    print p_q_2_close(n)
