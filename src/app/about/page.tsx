import '../globals.css';
import { Section, SectionHeading, SectionContent, Link } from '../utils';

export default async function Home() {

    return (
        <div className="text-center">
            <h1 className="text-4xl mt-5">
                About
            </h1>
            <Section>
                <SectionHeading>Overview</SectionHeading>
                <SectionContent>
                    Toronto has one of the largest shelter systems in the world.
                    The system is made up of various programs across the city, each offering
                    particular services. 
                    These services are administered by various groups, and the
                    capacity and occupancy of each is required to be tracked by 
                    the City. 
                </SectionContent>
            </Section>
            <Section>
                <SectionHeading>The data source</SectionHeading>
                <SectionContent>
                    This project explores the{' '} 
                    <Link url="https://open.toronto.ca/dataset/daily-shelter-overnight-service-occupancy-capacity/">
                        Daily Shelter & Overnight Service Occupancy & Capacity
                    </Link>
                    {' '}dataset publicized by Open Data Toronto.

                    This dataset provides information on shelter and overnight service programs ran by the City. 
                    There are various programs that are reported on, as outlined by the{' '}
                    <Link url="https://www.toronto.ca/city-government/data-research-maps/research-reports/housing-and-homelessness-research-and-reports/housing-stability-service-system-map-and-terms/">
                        Housing Stablity Service System Overview
                    </Link>
                    . This dataset is updated daily.
                </SectionContent>
                <SectionHeading>Data breakdown</SectionHeading>
                <SectionContent>
                    <b>Organizations</b><br/>Each shelter is run by an organization that provides the overnight service.<br/>
                    <b>Programs</b><br/>Programs are classified as either Emergency or Transitional.
                    <i> Emergency</i> programs can be accessed without a referral. 
                    <i> Transitional</i> programs provide required, specialized programming and can
                    be accessed by eligible individuals and families experiencing homelessness 
                    by referral only. <br/>
                    <b>Service type</b><br/>The type of service provided by the program. Types of service are:<br/>
                    <ul className='list-disc pl-8'>
                        <li>Shelter</li>
                        <li>24-Hour Respite</li>
                        <li>Motel/Hotel</li>
                        <li>Interim Housing</li>
                        <li>Warming Centre</li>
                        <li>24-Hour Women&apos;s Drop-in</li>
                        <li>Isolation/Recovery Site</li>
                    </ul>
                    <b>Shelter group</b><br/>Named for the lead shelter for which a program belongs to within the SMIS database. The group also includes other programs administered by the lead shelter<br/>

                </SectionContent>
            </Section>
        </div>
        
    );
};