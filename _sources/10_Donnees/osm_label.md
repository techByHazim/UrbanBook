
### Les équipements rétenus dans OpenStreetMap 

Dans cette section, je vous présente une autre source de données géographiques open source qu'on va utiliser dans notre projet : **OpenStreetMap (OSM)**.

OSM est une base de données géographique collaborative et libre. Elle contient des informations sur les infrastructures et services urbains, qui sont balisées par des **tags** (paires clé-valeur) dans la base de données. Pour plus d'informations sur les tags, vous pouvez consulter la documentation officielle d'OSM : [https://wiki.openstreetmap.org/wiki/Map_Features](https://wiki.openstreetmap.org/wiki/Map_Features).

Voici la liste des tags utilisés dans OpenStreetMap (**OSM**) pour extraire des données (géolocalisation) sur les divers infrastructures et services urbains actuellement retenus. Cette liste est non exhaustive et peut être complétée selon les besoins.

| Tags   | Label (FR)                                  |
| ----------------- | ------------------------------------------------ |
| transit_stop      | arrêt de transport (public)                      |
| bus_station       | gare routière                                    |
| bus_stop          | arrêt de bus                                     |
| public_transport  | transports en commun                             |
| bicycle_parking   | stationnement vélos / arceaux vélos              |
| gym               | salle de sport                                   |
| fitness_centre    | centre de fitness                                |
| sports_centre     | centre/complexe sportif                          |
| park              | parc                                             |
| pitch             | terrain de sport                                 |
| playground        | aire de jeux                                     |
| swimming_pool     | piscine                                          |
| garden            | jardin                                           |
| golf_course       | parcours de golf                                 |
| ice_rink          | patinoire                                        |
| dog_park          | parc canin                                       |
| nature_reserve    | réserve naturelle                                |
| marina            | port de plaisance                                |
| recreation_ground | terrain / espace de loisirs                      |
| fitness_station   | station de fitness en plein air                  |
| skateboard        | skatepark                                        |
| pub               | pub                                              |
| bar               | bar                                              |
| theatre           | théâtre                                          |
| cinema            | cinéma                                           |
| nightclub         | boîte de nuit / discothèque                      |
| events_venue      | salle d’événements / salle de spectacles         |
| restaurant        | restaurant                                       |
| cafe              | café                                             |
| food_court        | aire de restauration                             |
| marketplace       | marché / halle de marché                         |
| community_centre  | centre communautaire / maison de quartier        |
| library           | bibliothèque                                     |
| social_facility   | établissement / service social                   |
| social_centre     | centre social                                    |
| townhall          | mairie / hôtel de ville                          |
| school            | école                                            |
| childcare         | structure de garde d’enfants (crèche / garderie) |
| kindergarten      | école maternelle / jardin d’enfants              |
| university        | université                                       |
| college           | établissement d’enseignement supérieur (college) |
| pharmacy          | pharmacie                                        |
| dentist           | cabinet dentaire / dentiste                      |
| clinic            | clinique / centre médical                        |
| hospital          | hôpital                                          |
| doctors           | cabinet médical / médecins                       |
| musée             | musée                                            |
| place_of_worship  | lieu de culte                                    |


Ces tags seront utiliser dans des requêtes **Overpass API** pour extraire les données géographiques associées. La liste des clés et valeurs est disponible dans le fichier `proxy/data/raw/insee/overpass_config.json`.
Pour plus d'informations sur l'API Overpass, vous pouvez consulter la documentation officielle : [https://wiki.openstreetmap.org/wiki/Overpass_API](https://wiki.openstreetmap.org/wiki/Overpass_API).

L'extraction des données OSM fera l'objet de la section suivante.