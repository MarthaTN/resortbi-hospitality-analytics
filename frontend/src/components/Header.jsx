
import { useNavigate } from "react-router-dom";
import { useAuth } from "../auth/useAuth";

function Header() {
    const { logoutUser } = useAuth();
    const navigate = useNavigate();

    function handleLogout() {
        logoutUser();
        navigate("/login", { replace: true });
    }

    return (
        <header className="header">
            <div className="header-title">
                <span className="header-mark">RBI</span>
                <div><h1>Business Intelligence Portal</h1><p>Management insights from reservation data</p></div>
            </div>
            <button className="button button-secondary logout-button" onClick={handleLogout} type="button">Log out</button>
        </header>
    );
}

export default Header;
