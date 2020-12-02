# PR_LAB2

Pavlov Alexandru, FAF-181

***Structura generala la proiect***:
client1 - server1 - server3 - server2 - client2

server3 in mare parte e nevoie pentru a afisa clientii curent conectati, odata ce dau launch la client.py se trimite un ping mesaj si se salveaza intro lista numarul portului, care apoi poate fi transmisa la client in caz daca clientul il cere
numarul portului se foloseste ca 'numarul a clientului' care apoi poate fi apelat

Din cauza ca eu nu hardcodez porturile la clienti, sau n-am doua module diferite pentru ei, server3 poate fi perceput ca o carte de telefon dinamica

***Modulurile***

header_types.py - contine headerurile care sunt folosite pentru a se decide cum trebuie de actionat in urma primirii a unui mesaj trimis prin socket
  end_message si encrypted_end_message sunt pentru a afisa pe ecranul de output a clientului mesajul trimis(encrypted e pentru cazul in care doi clientii au fost conectati si mesajele trimise de catre ei trebuiesc decriptate)
  syn_message si syn_response sunt pentru a face procesul de handshake(are loc schimbul de chei partiale)
  delete_number pentru a sterge numarul din lista din server3 odata ce clientul decida sa iasa complet(deconectarea telefonului)
  lungimea la fiecare header = 5
  P.S. la moment deconectarea nu lucreaza complet
 
hamming.py - logica legata de hamming. Mereu, inainte de a transmite mesajul, sau dupa ce a fost acceptat, sunt chemate functiile din acest modul. 
  pe linga asta mai este o utiliy function pentru a converti mesajele intro secventa de bits, deoarece hammingul primeste ca input doar bits
  
client.py - modulul clientului, in el are loc crearea obiectului de tip application protocol

udpserver.py - launchul la server3 descris de mai sus. Ii fac bind, apoi dau launch la un select loop, pentru a putea accepta mesaje non-blocking. In mare parte anume pentru server3 non-blocking nu este tare nevoie

application_prot.py - parte la application level. In urma la init se face un socket nou(care joaca rolul in arhitectura client1 - server1), apoi folosesc un thread nou pentru a da launch la select_loop din transport_prot.py. In asa mod pot sa receptionez mesajele in mod non-blocking, fara chemarea explicita la recvfrom()
  Dupa ce fac launch la thread, trimit un mesaj de tip ping catre server3, apoi dau launch primul state - idle_listening.
  Anume din cauza ca state-urile reprezinta un while(True) loop, am fost nevoit sa recurg la crearea unui thread nou destinat pentru non-blocking listening
  idle_listening reprezinta momentul cind telefonul sta stationar. De aici clientul poate sau sa ridice 'trubka' sau sa raspunda la call(momentul cind clientul e sunat, se va afisa in consola clinetului)
  next state e main_client_loop. Aici clientul poate sa ceara de la server3 numarul(portul) la clientii conectati, sa sune la client sau sa iasa din retea(iesitul din retea la curent nu lucreaza stabil)
  on_call e state-ul in care are loc conversatia dintre clienti. Deoarece folosesc non-blocking, clientii nu sunt fortati sa vorbeasca pe rind. Tot contentul din mesaje este encriptat
  inainte de ca clientii sa treaca in on_call, are loc schimbul de chei partiale, cu metoda Diffie-Hellman.
  Pentru ca clientul sa poate accepta call-ul el din pacate e nevoit sa fie in idle_listening
  restul metodelor sunt pentru a face mai usor formarea mesajelor cu headeri
  
session_prot.py - session level. Aici sunt hardcodate doua numere prime pentru chei publice, si cheia privata, care se genereaza random, folosite pentru a calcula full chei. Metoda de encriptare e simpla, pur si simple adaug la ord() a fiecarui caracter din string valoarea la full key. La encriptare - invers. Metoda nu este cea mai buna, insa daca teoretic folosim numere prime extrem de mari, procesul poate dura un timp considerabil. Ca scop, cu ajutorul la diffie-hellman cheia private este protejata
  Tot aici se salveaza numarul(portul) a clientului cu care are loc convorbirea

transport_prot.py - la init se creeaza un socket UDP nou, se face init la session, apoi creez un selector. 
  bind_server - similar ca bind() default, il folosesc la server3
  close_sock - similar ca close() default
  select_loop - selector care imi permite sa primesc mesajele non-blocking, astfel e inregistrate o singura functie - receive_message
  receive_message - odata ce primeste un mesaj, trece prin hamming pentru a controla daca totul a ajuns intreg, scot headerul, si in dependenta de ce header e folosit, se executa instructiunile potrivite
  send_message - functie pentru a transmite mesajele
  
session_prot_util.py - functie pentru a genera un numar prim, folosit ca cheia privata

***Daca o sa doresti sai faci launch***
pornesti udpserver.py
pornesti doua instante de client.py
la una din ele faci primul input pck
tot la ea introduci req ca sa vezi portul la celalat client
introduci call
introduci numarul la client
la terminalul de la celalat clinet o sa se afiseze ca vine call
introduci res
ambii vor fi in on_call, poti liber sa scrii de la unul la altul
odata ce termini, introduci la ambii ext

In retea pot fi mai multi clienti, dupa ce se termina conversatia, poti suna pe altii
Nu se controleaza daca clientul la care suni deja vorbeste, sau daca numarul introdus nu este in retea
