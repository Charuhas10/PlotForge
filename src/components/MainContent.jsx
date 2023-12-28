import { useState } from "react";
import sendButtonIcon from "../assets/send-btn-icon.png";
import loadingIcon from "../assets/loading.svg";
import spooderMan from "../assets/spiderman.png";
import "../styles/MainContent.css";

const MainContent = () => {
  const [userInput, setUserInput] = useState("");
  const [synopsis, setSynopsis] = useState("");
  const [title, setTitle] = useState("");
  const [imageURL, setImageURL] = useState("");
  const [isLoading, setIsLoading] = useState(false);

  const generateContent = async () => {
    setIsLoading(true);
    setSynopsis(""); // Reset to ensure new data is distinct
    setTitle("");
    setImageURL("");

    try {
      console.log("Fetching data...");
      const res = await fetch("http://localhost:5000/generate", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ userInput }),
      });

      if (!res.ok) {
        throw new Error(`HTTP error! Status: ${res.status}`);
      }

      const data = await res.json();
      setSynopsis(data.synopsis);
      setTitle(data.title);
      setImageURL(data.imgURL);
      console.log(data);
      console.log("Title:", data.title);
      console.log("Synopsis:", data.synopsis);
      console.log("Image URL:", data.imgURL);
    } catch (error) {
      console.error("Error:", error);
    } finally {
      setIsLoading(false);
    }
  };

  const hasContent = title && synopsis && imageURL;

  return (
    <div className="main">
      {!hasContent && (
        <section id="setup">
          <div className="setup-inner">
            <img src={spooderMan} alt="Spiderman" />
            <div className="speech-bubble" id="speech-bubble">
              <p id="bubble-text">
                {/* eslint-disable-next-line*/}
                Do you have a movie plot in mind? Tell me about it, and I'll
                bring it to life!
              </p>
            </div>
          </div>
          <div className="setup-inner setup-input" id="setup-input">
            <textarea
              id="setup-textarea"
              value={userInput}
              onChange={(e) => setUserInput(e.target.value)}
            ></textarea>
            <button
              className="send-btn"
              id="send-btn"
              aria-label="send"
              onClick={generateContent}
            >
              {isLoading ? (
                <img src={loadingIcon} alt="Loading" />
              ) : (
                <img src={sendButtonIcon} alt="Send" />
              )}
            </button>
          </div>
        </section>
      )}

      <section
        className="output"
        id="output"
        style={{ display: hasContent ? "block" : "none" }}
      >
        {isLoading ? (
          <img src={loadingIcon} alt="Loading" className="loading" />
        ) : (
          hasContent && (
            <div>
              {console.log("Rendering Content")}
              <div id="output-img" className="output-img">
                <img src={imageURL} alt="Generated Visual" />
              </div>
              <div>
                <h1 id="output-title">{title}</h1>
                <p id="output-text">{synopsis}</p>
              </div>
            </div>
          )
        )}
      </section>
    </div>
  );
};

export default MainContent;
