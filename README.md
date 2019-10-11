## Gianluca Scarpellini - Università degli studi di Milano - Bicocca - "Riconoscimento oggetti da flussi dati RGB e LIDAR" - luglio 2018

## Abstract


La computer vision in ambito automotive ha visto un crescente interesse delle aziende
negli ultimi anni (es. progetto Waymo, Google, 2009). Aziende hardware e software stanno
focalizzando la loro attenzione su nuovi sensori e tecnologie di visione che affianchino le
camere tradizionali. Tra i sensori più utilizzati in questo ambito, ci sono i laser scanner
(LIDAR), i quali sono in grado di generare una rappresentazione dello spazio circostante in
3D sotto forma di nuvola di punti. Di conseguenza, sta emergendo chiaramente la necessità
di strumenti adatti a interpretare nuove tipologie di dati e ricavarne informazioni. La
computer vision ha avuto una rapida evoluzione nell’ultimo decennio e, con l’introduzione
di Reti Neurali Convoluzionali (Alexnet, 2012), ha raggiunto livelli di precisione prima
inaspettati. La tesi inizia con la descrizione del flusso dati LIDAR, e delle problematiche
legate suo impiego per l’object detection. Il progetto di tesi ha previsto lo sviluppo di una
pipeline di conversione che ha permesso di generare l’immagine di depth a partire dai dati
grezzi point-cloud provenienti dal LIDAR. A questa fase, è seguita una fase di studio delle
idee cardine delle reti artificiali specializzate nella detection di oggetti. In particolare è
stato scelto di approfondire YOLO (Redmon et. al., 2016 [8]). L’implementazione YOLO
per il framework pytorch è stata estesa all’interno della tesi all’impiego di dati RGB-D e
addestrata sul dataset Kitti Vision Benchmark Suite, il quale è un progetto open source
liberamente accessibile che mette a disposizione immagini RGB e dati LIDAR acquisiti
strada in ambiente non controllato. I risultati ottenuti sono infine presentati suddividendoli
in tre classi di difficoltà: easy, moderate, e hard.

## Contattami
- github: gianscarpe
- mail: gianluca[at]scarpellini.dev or g.scarpellini1[at]campus.unimib.it
