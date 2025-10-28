import { Button } from "@mui/material";

// runs at build time 
//export async function getStaticProps() {
//  const res = await fetch('../public/toronto-skyline.jpg');
//}

export default async function Home() {
  return (
    <div className="grid grid-cols-1 text-center content-center relative bg-blue">
      <figure>
        <figcaption>
          <div className="relative">
            <img src={'/toronto-skyline.jpg'} alt="Toronto skyline from Broadview avenue" className="w-full z-1" />
            <div className="absolute bg-blue w-full h-full top-0 left-0"/>
          </div>
          <span>&quot;Toronto Skyline&quot; by jareed. </span>
          <i>Licensed under CC BY 2.0. To view a copy of this license, visit https://creativecommons.org/licenses/by/2.0/?ref=openverse.</i>
        </figcaption>
      </figure>
      
      <div className="absolute inset-y-50 inset-x-50 text-yellow-400 font-bold">
        <h1 className="text-5xl p-5">Toronto Shelter Occupancy Application</h1><br/>
      </div>
      <div className="flex items-center justify-center gap-4 p-10">
        <Button variant="contained" size="large" className="" href="/story">Read my analysis of the data</Button>
        <Button variant="contained" size="large" href="/about">Understand the background of the project</Button>
      </div>
      
    </div>
  );
}
