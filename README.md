# Evolving Fuzzy System for Real-Time Monitoring and Adaptation: Novelty Detection and Cluster Updating
> The aim of the project is to develop a fuzzy logic algorithm that receives real-time information from a wastewater treatment plant (WWTP) and provides a reference value for the Multi-layer Stream Mapping (MSM) performance evaluation method.


## Table of Contents
* [General Info](#general-information)
* [Technologies Used](#technologies-used)
* [Features](#features)
* [Screenshots](#screenshots)
* [Setup](#setup)
* [Usage](#usage)
* [Project Status](#project-status)
* [Room for Improvement](#room-for-improvement)
* [Acknowledgements](#acknowledgements)
* [Contact](#contact)
<!-- * [License](#license) -->


## General Information
- This work is being carried out within the scope of the PhD programme in Electrical Engineering and Intelligent Systems at the University of Coimbra in Portugal..
- The programme aims to receive samples of physical and chemical characteristics, in real time, from a wastewater treatment plant, represented by the BSM2 simulator, and provide reference values for the Multi-layer Stream Mapping (MSM) performance evaluation system.
- The fuzzy system starts the process with just one cluster, represented by the first sample that arrives in the model. When new samples arrive, they are processed and if they represent something new in relation to the existing cluster, new clusters are created. If they don't represent anything new, they are sent back to the existing cluster.
- As samples are constantly arriving, they are processed, used to create or update the clusters, and then discarded. 
<!-- You don't have to answer all the questions - just the ones relevant to your project. -->


## Technologies Used
- Python - version 3.8.8
- Benchmark Simulation Model no. 2 (BSM2)



## Setup
* To run the case study script, all you need is Python and the Spyder editor installed.
* To obtain the used datasets, install and run the BSM2 simulator. More details about the installation and operation of BSM2 can be found here https://github.com/wwtmodels and here https://wwtmodels.pubpub.org.


## Project Status
The project is in progress.


## Acknowledgements
* This research is supported by Fundação para a Ciência e a Tecnologia (FCT) under the grant ref. 2023.01009.BD.
* Institute of Systems and Robotic - ISR 
* DEEC - University of Coimbra - Portugal.



## Contact
Rodrigo Salles. Email: engenharia.salles@gmail.com 

...feel free to contact me!


<!-- Optional -->
<!-- ## License -->
<!-- This project is open source and available under the [... License](). -->

<!-- You don't have to include all sections - just the one's relevant to your project -->
