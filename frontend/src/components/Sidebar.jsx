
import { NavLink } from "react-router-dom";
import { useAuth } from "../auth/useAuth";

const links = [
    { to: "/dashboard", label: "Dashboard", symbol: "▦", managementOnly: true },
    { to: "/revenue", label: "Revenue", symbol: "↗", managementOnly: true },
    { to: "/occupancy", label: "Occupancy", symbol: "▤" },
    { to: "/visitors", label: "Visitors", symbol: "◎" },
    { to: "/reports", label: "Reports", symbol: "▧", managementOnly: true },
    { to: "/settings", label: "Settings", symbol: "⚙" },
];

function Sidebar() {
    const { isManagement } = useAuth();
    const visibleLinks = links.filter((link) => !link.managementOnly || isManagement);
    return (
        <aside className="sidebar">
            <div className="sidebar-logo"><div className="logo-mark">R</div><div><strong>ResortBI</strong><span>HOSPITALITY BI</span></div></div>
            <p className="nav-caption">WORKSPACE</p>
            <nav aria-label="Main navigation">
                {visibleLinks.map((link) => (
                    <NavLink key={link.to} to={link.to} className={({ isActive }) => `nav-link${isActive ? " active" : ""}`}>
                        <span className="nav-symbol" aria-hidden="true">{link.symbol}</span><span>{link.label}</span>
                    </NavLink>
                ))}
            </nav>
            <div className="sidebar-footer"><span className="online-dot" /> Local development portal</div>
        </aside>
    );
}

export default Sidebar;
