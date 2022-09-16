import * as React from "react";

const SVGComponent = (props) => (
  <svg
    xmlSpace="preserve"
    viewBox="0 0 100 100"
    y={0}
    x={0}
    xmlns="http://www.w3.org/2000/svg"
    {...props}
    width="30%"
  >
    <g
      style={{
        transformOrigin: "50% 50% 0px",
        transform: "rotate(0deg) scale(0.8)",
      }}
      className="ldl-scale"
    >
      <g className="ldl-ani">
        <g className="ldl-layer">
          <g
            className="ldl-ani"
            style={{
              transform: "scale(0.91)",
              transformOrigin: "50px 50px 0px",
              animation:
                "1.11111s linear -0.740741s infinite normal forwards running breath",
            }}
          >
            <path
              fill="#acbd81"
              d="M75.4 11.5h-56c-1.1 0-2 .9-2 2v60.1c0 .8.7 1.5 1.5 1.5H20v14.5h-1.1c-.8 0-1.5.7-1.5 1.5s.7 1.5 1.5 1.5h56.5c4 0 7.2-3.2 7.2-7.2V18.7c0-4-3.2-7.2-7.2-7.2z"
              style={{
                fill: "rgb(172, 189, 129)",
              }}
            />
          </g>
        </g>
        <g className="ldl-layer">
          <g className="ldl-ani">
            <g>
              <g className="ldl-layer">
                <g
                  className="ldl-ani"
                  style={{
                    transform: "scale(0.91)",
                    transformOrigin: "50px 50px 0px",
                    animation:
                      "1.11111s linear -0.925926s infinite normal forwards running breath",
                  }}
                >
                  <path
                    fill="#f4e6c8"
                    d="M72.8 89.5H20V75h52.8c4 0 7.2 3.2 7.2 7.2 0 4.1-3.2 7.3-7.2 7.3z"
                    style={{
                      fill: "rgb(244, 230, 200)",
                    }}
                  />
                </g>
              </g>
            </g>
          </g>
        </g>
        <g className="ldl-layer">
          <g
            className="ldl-ani"
            style={{
              transform: "scale(0.91)",
              transformOrigin: "50px 50px 0px",
              animation:
                "1.11111s linear -1.11111s infinite normal forwards running breath",
            }}
          >
            <path
              fill="#e15c64"
              d="M41.8 37l-7.1-7.1c-.3-.3-.7-.3-.9 0L26.6 37c-.4.4-1.1.1-1.1-.5V8.2c0-.4.3-.7.7-.7h16c.4 0 .7.3.7.7v28.5c0 .5-.7.8-1.1.3z"
              style={{
                fill: "rgb(225, 92, 100)",
              }}
            />
          </g>
        </g>
      </g>
    </g>
  </svg>
);

export default SVGComponent;
