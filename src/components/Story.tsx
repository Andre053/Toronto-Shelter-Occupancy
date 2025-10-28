'use client'
import { LineChart } from '@/components/LineChart';
import { GraphData, GeoData, AllStatsFsa, ShelterDataList } from '@/types/types';
import { useState, useEffect } from 'react';
import { Section, SectionHeading, SectionSubHeading, SectionContent, Link, setJsonData, filterFsaStats } from '@/app/utils';
import { ShelterMap } from '@/components/Map';
import { FeatureCollection } from 'geojson';
import { MultiLineChart } from '@/components/MultiLineChart';

export default function Story() {
    const [chartDailyUserCount, setChartDailyUserCount] = useState<GraphData | null>(null);
    const [mapFsa, setMapFsa] = useState<FeatureCollection | null>(null);
    const [mapNeighbourhoods, setMapNeighbourhoods] = useState<FeatureCollection | null>(null);
    const [mapShelters, setMapShelters] = useState<FeatureCollection | null>(null);
    const [overallFsaStats, setOverallFsaStats] = useState<AllStatsFsa[] | null>(null);
    const [activeSheltersDaily, setActiveSheltersDaily] = useState<GraphData | null>(null);
    const [activeOrgsDaily, setActiveOrgsDaily] = useState<GraphData | null>(null);
    const [activeProgramsDaily, setActiveProgramsDaily] = useState<GraphData | null>(null);
    const [activeProgramsEmerg, setActiveProgramsEmerg] = useState<GraphData | null>(null);
    const [activeProgramsTrans, setActiveProgramsTrans] = useState<GraphData | null>(null);
    const [shelterData, setShelterData] = useState<ShelterDataList | null>(null);

    useEffect(() => {
        if (chartDailyUserCount || mapShelters) return;
        setJsonData('/chart/daily_service_user_count.json', setChartDailyUserCount)
        setJsonData('/chart/daily_active_shelters.json', setActiveSheltersDaily)
        setJsonData('/chart/daily_active_orgs.json', setActiveOrgsDaily)
        setJsonData('/chart/daily_active_programs.json', setActiveProgramsDaily)
        setJsonData('/chart/daily_emergency_programs.json', setActiveProgramsEmerg)
        setJsonData('/chart/daily_transitional_programs.json', setActiveProgramsTrans)

        setJsonData('/map/tor_fsa_cbf.geojson', setMapFsa);
        setJsonData('/map/tor_neighbourhoods.geojson', setMapNeighbourhoods)
        setJsonData('/map/shelters.geojson', setMapShelters)
        setJsonData('/map/overall_fsa_stats.json', setOverallFsaStats)

        setJsonData('/map/data_by_shelter.json', setShelterData)

    }, [chartDailyUserCount, mapShelters])


    return (
        <div className="text-center">
             <h1 className="text-4xl p-5">
                Data Story
            </h1>
            <Section>
                <SectionHeading>Introduction</SectionHeading>
                <SectionContent>
                    In May 2023, Toronto City Council declared a homelessness emergency. 
                    
                    According to the Street Needs Assessment by the City of Toronto (2024), there was an estimated total of 15,418 homeless people within the city in October 2024 -- over double the amount of the same estimate made in April 2021. 

                    This number is the sum of all homeless people in city-administered and provincially administered sites, in addition to an estimate of those living outside of the system. Of this number, city-administered sites made up 80% of all those within the system. 

                    The city-administered shelter system has increased capacity as demand for shelters have grown. 

                    The city views homelessness as &quot;the result of failures across multiple systems, such as housing, 
                    health care, mental health, income support, and the justice system&quot; (2024 Street Needs Assessment). 
                    Within this context, the shelter system is seen as the last resort for the victims of these failures. 

                    Toronto operates the largest shelter system in Canada. 
                </SectionContent>
                <SectionContent>
                    In this project, I look to analyze the occupancy data provided by the City. I collected the data from the start of collection, in January 2021, to the beginning of October 2025.
                </SectionContent>
            </Section>
            <Section>
                <SectionHeading>Highlights</SectionHeading>
                <SectionSubHeading>Trends</SectionSubHeading>
                {chartDailyUserCount && (
                    <>
                        <LineChart data={chartDailyUserCount} stat='Daily Service User Count' title='Rising service user count until early 2025'/>
                        <SectionContent>
                            From the start of the data collection, there has been a gradual rise of 
                            average service users until a sharp trend downwards in early 2025.

                            At the start of 2021, there was around 6,000 average service users a day within the system.
                            This increased by over 1,000 people the next year, over 2,000 more the next, and by 2024 
                            there was consistently over 9,500 people within the system. The start of 2025 say the highest 
                            numbers yet, but then a sharp decline began. By October this year, the average was down to below
                            9,000 people on average. 

                        </SectionContent>
                    </>
                    
                )}
                {activeOrgsDaily && (
                    <>
                        <LineChart data={activeOrgsDaily} stat='Active Organizations' title='Active organizations shows little change'/>
                        <SectionContent>
                            The number of active organizations has been either 34 or 35 for most of the last 4 years. Beginning in Spring 2024
                            there seems to be a slight gradual increase in active organizations, with 39 active as of October 2025. 
                        </SectionContent>
                    </>
                )}
                {activeSheltersDaily && (
                    <>
                        <LineChart data={activeSheltersDaily} stat='Active Shelters' title='Active shelters has remained consistent'/>
                        <SectionContent>
                            Throughout this period, the number of active shelters within the city has remained around 100. At the beginning
                            of each year, a termporary increase in shelters can be seen -- a result of the creation of warming centres during
                            the colder Winter months. 
                        </SectionContent>
                    </>
                )}
                {activeProgramsEmerg && activeProgramsTrans && (
                    <>
                        <MultiLineChart data={[activeProgramsEmerg, activeProgramsTrans]} stat='Active Programs' title='Active emergency programs have flucuated recently'/>
                        <SectionContent>
                            Diving into these numbers further, it appears the start of 2025 also saw a flucuation in active emergency programs. 
                            Active transitional programs have been stable until the recent gradual increase beginning in Fall 2024. Active emergency
                            programs have been less consistent, but increases can be seen during Winter months, as seen in the number of active shelters. 
                            The outlier is 2025, where flucuations previously unseen occurred starting around November 2024 and ending around May 2025. 
                            This is followed by another flucuation between late June and early September, ending with the lowest number of emergency programs
                            within the data. 
                        </SectionContent>
                    </>
                )}
                <SectionSubHeading>Mapping</SectionSubHeading>
                <SectionContent>
                    The City of Toronto can be organized by Forward Sortation Addresses (FSA). These are the first 3 character codes that are 
                    part of all Canadian postal codes; each FSA is determined by the government, typically based off of the number of people
                    living within the area: generally, FSA areas near downtown Toronto will be geographically smaller than those further away.
                    Since the open data already provides postal code information for each data point, I decideded to use them as a way
                    to visualize the city.
                </SectionContent>
                {mapShelters && mapFsa && overallFsaStats && (
                    <>
                        <ShelterMap geoData={mapFsa} shelterData={mapShelters} title="Average service user count by FSA" statName="Service users" heatData={filterFsaStats(overallFsaStats, 'MEAN_SERVICE_USERS')}/>
                        <SectionContent>
                            This map is coloured based on the average number of daily service users within each FSA area, with darker red areas having a 
                            higher average; gray areas are those that
                            do not appear in the dataset. The map also has yellow points at each of the shelter locations within the city. There appears 
                            to be some mismatch between the dataset and the FSA areas of Toronto as various shelters are plotted within FSA areas that 
                            have no associated data within the dataset. Further investigation is needed, but a potential cause of this may be due to 
                            incorrect input of postal codes into the database. Another note is that this map depicts shelters that were active at any 
                            time throughout the data, so shelters that have since closed or moved will all appear.<br/>
                                Analyzing this map, there is a large concentration of shelters downtown, with others scattered throughout the city. 
                            The FSA with the highest average daily shelter users is M5A, right downtown, with over 945 people there on average over the
                            last 4 years. Surprisingly, M2J is next, with 911 average service users, followed by M9W with 667. Though this map shows a 
                            high level overview, since the data shown is so broad a lot of insights are missed. 

                        </SectionContent>
                    </>
                )}
            </Section>
           
            <Section>
                <SectionHeading>References</SectionHeading>
                <SectionContent>
                    2024 Street Needs Assessment. City of Toronto. https://www.toronto.ca/wp-content/uploads/2025/07/9790-street-needs-assessment-report-2024.pdf
                </SectionContent>
            </Section>
        </div>
        
    );
};

/**

 <Section>
                <SectionHeading>Number of locations over time</SectionHeading>
                <SectionContent>
                    Toronto currently shows [97] locations active and running programs.
                </SectionContent>
            </Section>
            <Section>
                <SectionHeading>Concentrations of occupied rooms vs. beds</SectionHeading>
            </Section>


 */

