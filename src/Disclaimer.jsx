import React from "react";
import { Typography } from "@material-ui/core";

const styles = {
  contact: {
    padding: "50px",
    textAlign: "center",
    backgroundColor: "#46282d",
    color: "white",
  },
};

export default class Disclaimer extends React.Component {
  render() {
    return (
      <div style={styles.contact}>
        <h1>Contact Us Page</h1>

        <Typography>
          사이트 이용 시 일부 수수료를 받을 수 있음
        </Typography>
      </div>
    );
  }
}
