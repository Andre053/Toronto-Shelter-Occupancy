'use client'
import Link from "next/link"
import { FaGithub } from 'react-icons/fa';

const LinkItem = ({children, href}: {children: React.ReactNode; href: string; }) => (
    <Link
        href={href}
        className="hover:font-bold"
    >
        {children}
    </Link>
)

export const NavBar = () => (
    <nav className="z-5 sticky top-0 w-full flex items-center justify-between bg-blue-500 p-2 mb-2 text-2xl text-white font-semibold border-b-2 border-indigo-400">
        <Link href="https://github.com/Andre053/Toronto-Shelter-Occupancy" className="ml-5">
            <FaGithub/>
        </Link>
        <ul className="flex items-center gap-8 mt-2 mb-2 mr-5">
            <Link href="/story" className="hover:font-bold">
                Story
            </Link> 
            <Link href="/about" className="hover:font-bold">
                About
            </Link>              
        </ul>
    </nav>
)