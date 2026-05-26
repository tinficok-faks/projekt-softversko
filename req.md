# Projekt: Helpdeskt / ticketing sustav
## Članovi tima
- Dominik Karimović
- Tony Vargek
- Tin Fićok
- Petar Mikolčević
- Antonio Meleš

## GitHub repozitorij
- Link: https://github.com/TonyVargek/projekt-softversko
- Svi članovi dodani: DA

## User storyji
US-01 Kao user, želim se moći prijaviti i ostaviti ticket (zatražit pomoć).
      kako bih mogao doći u kontakt s IT službom.<br>
US-02 Kao user, želim moći vidjet status svog ticketa (delivered, seen, assigned, solved).<br>
US-03 Kao support, želim se moći prijaviti i vidjeti sve tickete stavljene od usera
      kako bi ih mogao rješiti.<br>
US-04 Kao admin, želim se moći prijaviti i assignati tickete supportu kako bi ih
      mogli rješiti.<br>
US-05 Kao admin, želim moći dodati prioritet ticketa.
## Funkcijski zahjtevi
FZ-01 Sustav mora omogućiti prijavu.<br>
FZ-02 Sustav omogućuje tri razine pristupa (korisnik, support, admin).<br>
FZ-03 Sustav mora omogućiti useru da doda ticket (dodati naslov, opis problema, eventualno attachment).<br>
FZ-04 Sustav nakon poslanog ticketa od usera mora vratiti povratnu informaciju da je ticket zaprimljen.<br>
FZ-05 Sustav mora omogućiti vidljivost statusa svog ticketa.<br>
FZ-06 Sustav mora omogućiti supportu vidljivost ticketa koji su mu assigned.<br>
FZ-07 Sustav mora omogućiti adminu da sortira tickete po vremenu primitka.<br>
FZ-08 Sustav mora omogućiti adminu da dodjeli supportu određeni ticket.<br>
FZ-09 Sustav mora omogućiti adminu da doda prioritet ticketa.<br>
FZ-10 Sustav mora spriječiti dodjeljivanje istog ticketa više članova supporta.<br>

## Nefunkcijski zahtjevi
NZ-01 Sustav očitava X ticketa unutar 2s vremena u 95% slučajeva.<br>
NZ-02 Odgovor korisniku mora biti vidljiv unutar aplikacije bez iznimke.<br>
NZ-03 Sustav zahtjeva prijavu svakih 30 minuta<br>
NZ-04 Sustav mora biti oblikovan kao microservice i containerizied.<br>
NZ-05 Kreiranje ticketa mora biti ispod 5 koraka.<br>
NZ-06 Sustav mora proći preko 95% testova.<br>
NZ-07 Sustav ne smije uzeti više od 5 minuta slanja ticketa, te vraćanja odgovora.<br>


## Taskovi
TASK-01 Napraviti model baze za helpdesk / ticketing sustav<br>
TASK-02 Implementirati API endpoint ticket<br>
TASK-03 Implementirati API endpoint user<br>
TASK-04 Implementirati API endpoint support<br>
TASK-05 Implementirati API endpoint admin<br>
TASK-06 Napisati testove za sustav/kod<br>
TASK-07 Implementirati autorizaciju korisnika<br>
TASK-08 Containerize aplikaciju<br>
TASK-09 Kreirati sučelje<br>

## Raspodjela zadataka
Dominik: TASK-07, TASK-09, NZ-05, NZ-03, FZ-01, FZ-02<br>
Petar: TASK-06, NZ-01, NZ-06, FZ-04, FZ-05, FZ-06<br>
Antonio: TASK-01, TASK-08, NZ-04, FZ-03, FZ-06, FZ-10<br>
Tin: TASK-04, TASK-05, NZ-07, FZ-04, FZ-07, FZ-10<br>
Tony: TASK-02, TASK-03, NZ-02, FZ-03, FZ-08, FZ-09<br>
