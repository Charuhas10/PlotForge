import "../styles/Header.css";
import logo from "../assets/logo-movie.png";

function Header() {
  return (
    <div id="header">
      <img src={logo} alt="PlotForge" />
      <a href="/">
        <span>Plot</span>Forge
      </a>
    </div>
  );
}

export default Header;
