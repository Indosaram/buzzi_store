import React from "react";
import { makeStyles } from "@material-ui/core/styles";

const useStyles = makeStyles(() => ({
  contact: {
    // margin: "0 10% 0",
    background: "linear-gradient(45deg, #FE6B8B 30%, #FF8E53 90%)",
    padding: "0 30px",
    color: "white",

  },
  contact__heading: {
    textAlign: "center",
    fontFamily: "paybooc-Bold",
  },
  contact__body: {
    textAlign: "left",
    fontFamily: "paybooc-Medium",
  },
}));

const Contact = () => {
  const classes = useStyles();
  return (
    <div className={classes.contact}>
      <h1 className={classes.contact__heading}>Contact us!</h1>
      <p className={classes.contact__body}>
        사용 중 불편사항이나 문의사항이 있으시면 페이지 우측 하단의 채널톡을
        이용해 주시기 바랍니다.
      </p>
    </div>
  );
};

export default Contact;
