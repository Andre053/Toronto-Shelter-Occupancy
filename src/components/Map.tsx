'use client'
import { useEffect, useInsertionEffect, useRef, useState } from "react";
import { geoPath, geoCircle, } from "d3";
import { FeatureCollection } from "geojson";
import '../app/globals.css';
import { GeoData, HeatmapData, AllStatsFsa } from "@/types/types";
import * as d3 from "d3";

type PropsMap = {
    geoData: FeatureCollection;
    shelterData: FeatureCollection;
    heatData?: HeatmapData;
    statName?: string;
    title: string;
}

const getColour = (colourStart: string, colourEnd: string, value: number, max: number, min: number) => {
    const colourScale = d3.scaleLinear([min, max], [colourStart, colourEnd])
    return colourScale(value)
}
const setPathColour = (data: HeatmapData, gRef: any) => {
    const g = d3.select(gRef.current); // should only be a single g tag

    g.selectAll('.fsaPath') // go through all paths and change the colour
        .classed('stroke-black', true)
        .attr('fill', (d: any) => {
            const fsa: string = d.properties.CFSAUID;
            const fsaData = data.stats[fsa];
            if (fsaData) return getColour('#fdbb84', '#e34a33', fsaData, data.statMax, data.statMin);
            return 'gray';
        })
    g.style('visibility', 'visible') // make visible once recoloured
}

// adding gradients
// for each point, want a circle around it, static size, gradient 


export function ShelterMap({geoData, shelterData, title, heatData, statName}: PropsMap) {
    const width = 1000;
    const height = 800;

    const [zoomTransform, setZoomTransform] = useState(null);
        
    const geoProjection = d3.geoMercator()
        .fitSize([width/1.5, height/2], geoData);

    const geoGenerator = geoPath()
        .projection(geoProjection)
        .pointRadius(2.5);
    
    const svgRef = useRef<SVGSVGElement | null>(null);
    const gRef = useRef<SVGGElement | null>(null);

    const zoom: any = d3.zoom()
        .scaleExtent([1, 5]) // TODO: Get best scale extent
        .on("zoom", (e) => { 
            setZoomTransform(e.transform)
        });
    const mouseOverPath = (e: any) => {
        d3.selectAll('.fsa-path')
            .transition()
            .duration(200)
            .style('opacity', .8)
        d3.select(e.target)
            .transition()
            .duration(200)
            .style('opacity', 1)
            .style('stroke', 'black')
        d3.select('#tooltip-div')
            .text(`${e.target.attributes[0].value} ${heatData && statName ? " - " + statName + ": " + heatData.stats[e.target.attributes[0].value] : ''}`)
    };
    const mouseLeavePath = (e: any) => {
        d3.selectAll('.fsa-path')
            .transition()
            .duration(200)
            .style('opacity', 1)
        d3.select(e.target)
            .transition()
            .duration(200)
    };
    const mouseClickPath = (e: any) => {
        // TODO: Keep the target selected on the map once clicked, until a new one is clicked
        d3.select(e.target)
            .transition()
            .duration(800)
            .style('opacity', 1)
            .style('stroke', 'green')
            .attr('id', 'fsa-selected') // sets to selected
    };
    // does nothing
    const mouseOutPath = (e: any) => {
        d3.selectAll('.fsa-path') 
            .style('stroke', 'black')
    };
    const mouseOverShelter = (e: any) => {
        d3.select(e.target)
            .transition()
            .duration(200)
            .style('opacity', 1)
        d3.select('#tooltip-div')
            .text(`${e.target.attributes[1].value}`)
    };
    const mouseOutShelter = (e: any) => {
        d3.selectAll('.shelterPath')
            .transition()
            .duration(200)
        d3.select(e.target)
            .transition()
            .duration(200)
    };
    const mouseOverG = (e: any) => {
        d3.select('#tooltip-div')
            .style('visibility', 'visible');
    };
    const mouseMoveG = (e: any) => {
        const scroll = window.scrollY
        d3.select('#tooltip-div')
            .style('top', (e.clientY-25+scroll)+'px') // get position on entire page
            .style('left', (e.clientX+10)+'px');
    };
    const mouseOutG = (e: any) => {
        d3.select('#tooltip-div')
            .style('visibility', 'hidden');
    };

    // likely not needed for geo heatmap
    const quardSearch = (quadtree: d3.Quadtree<number>, x0: number, y0: number, x3: number, y3: number) => {
        const validData: any = []
        quadtree.visit((node: any, x1, y1, x2, y2) => {
            const p = node.point;
            if (p) {
                p.selected = (p[0] >= x0) && (p[0] < x3) && (p[1] >= y0) && (p[1] < y3);
                if (p.selected) {
                    validData.push(p);
                }
            }
            return x1 >= x3 || y1 >= y3 || x2 < x0 || y2 < y0;
            });
        return validData;
    }

    useEffect(() => {
        if (!geoData || !shelterData || !width || !height) return;
        
        const svg = d3.select(svgRef.current)
            .style('position', 'relative');
            
        const g = d3.select(gRef.current)
            .attr('id', 'map-group')
            .style('position', 'relative')

        svg.node()?.addEventListener('wheel', (e) => {
            e.preventDefault()
        }, { passive: false });

        svg
            .attr('width', width/1.5)
            .attr('height', height/2)
            .call(zoom);

        // add the tooltip div 
        // where the div is appended matters
        // the SVG element does not know how to handle a div
        d3.select('body') 
            .append('div')
            .attr('id', 'tooltip-div')
            .style('position', 'absolute')
            .style('visibility', 'hidden')
            .style('font-weight', 'bold')
            .style('background-color', 'white')
            .style('padding', '1px')
            .style('color', 'black')
            .style('border', 'solid')
            .style('z-index', 2)

        g.selectAll('*').remove(); // remove all path elements when geodata changed

        // add tooltip functionality
        g.on('mouseover', mouseOverG)
            .on('mousemove', mouseMoveG)
            .on('mouseout', mouseOutG);

        g.selectAll('.fsaPath')
            .data(geoData.features)
            .enter()
            .append('path')
                .attr('key', (d) => d.properties?.CFSAUID)
                .attr('d', geoGenerator)
                .attr('class', 'fsa-path')
                .attr('fill', 'lightgray') // have original map be white? gray?
                .attr('class', 'fsaPath')
                .style('stroke', 'black')
                .on('mouseover', mouseOverPath)
                .on('mouseleave', mouseLeavePath)
                .on('click', mouseClickPath)
                .on('mouseout', mouseOutPath)

        // plot shelters with address key
        g.selectAll('.shelterPath')
            .data(shelterData.features)
            .enter()
            .append('path')
                .attr('d', geoGenerator)
                .attr('key', (d) => {
                    return d.properties?.address // properties are address, id, name, org, program
                })
                .attr('r', 0)
                .attr('class', 'shelter-path')
                .attr('fill', 'yellow')
                .style('stroke', 'orange')
                .style('opacity', 0.85)
                .on('mouseover', mouseOverShelter)
                .on('mouseout', mouseOutShelter)
            
        if (heatData) setPathColour(heatData, gRef); // colour the map

        // clustering
        const clusterPoints = [];
        const clusterRange = 50;

        const pointsRaw = shelterData.features.map((d, i) => {
            const point = geoGenerator.centroid(d);
            point.push(i);
            return point;
        })
        const quadtree: any = d3.quadtree(pointsRaw)

        for (let x=0; x <= width; x += clusterRange) {
            for (let y=0; y <= height; y += clusterRange) {
                const searched = quardSearch(quadtree, x, y, x+clusterRange, y+clusterRange)

                const centre = searched.reduce((prev: any, cur: any) => {
                    return [prev[0] + cur[0], prev[1] + cur[1]]
                }, [0,0])

                centre[0] = centre[0] / searched.length
                centre[1] = centre[1] / searched.length

                if (centre[0] && centre[1]) {
                    clusterPoints.push(centre)
                    console.log('Added cluster', {centre})
                }
            }
        }
        g.selectAll(".centre-point")
            .data(clusterPoints)
            .enter()
            .append('circle')
                .attr('class', 'centre-point')
                .attr('cx', (d) => d[0])
                .attr('cy', (d) => d[1])
                .attr('fill', 'lightblue')

     }, [geoData, width, height]);

     useEffect(() => {
        const g = d3.select(gRef.current);
        g.attr('transform', zoomTransform);
     }, [zoomTransform])

    // TODO: Improve spacing of info elements
    // TODO: Add colour legend when fixed
    // ColourLegend lowColour={'#ebc034'} highColour={'#eb4034'} maxVal={fsaStats.max} minVal={0}/>
    const styles = `relative justify-center z-1 grid col-span-1`
    return (
        <>
            <h1 className="text-2xl my-3 text-center">{title}</h1>
            <div id='map-container' className={styles}>
                <svg ref={svgRef} className="border border-5 border-gray-500 rounded-3xl m-2">
                    <g ref={gRef} />
                </svg>
            </div>
        </>
    )
}