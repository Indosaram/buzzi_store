import React from "react";
import { makeStyles } from "@material-ui/core/styles";

const useStyles = makeStyles(() => ({
  contact: {
    textAlign: "center",
    fontFamily: "paybooc-Medium",
    margin: "0 10% 0",
  },
  h1: {
    fontFamily: "paybooc-Bold",
    color: "#FE6B8B",
    fontWeight: 800,
  },
  h2: {
    color: "#FF8E53",
    fontSize: 18,
    fontWeight: 500,
  },
  logo: {
    maxWidth: 120,
  },
  body: {
    textAlign: "justify",
  },
}));

const About = () => {
  const classes = useStyles();

  return (
    <React.Fragment>
      <div className={classes.contact}>
        <h1 className={classes.h1}>What is Buzzi.Store?</h1>
        <h2 className={classes.h2}>"실시간 핫딜정보 플랫폼"</h2>
        <div className={classes.body}>
          <p>
            뽐뿌, 루리웹, 쿨앤조이 등 사이트의 핫딜 정보를 실시간으로
            큐레이션해서 제공합니다. 품절되거나 중지된 딜은 목록에서 자동으로
            삭제됩니다.
          </p>
          <p>
            원본 게시물을 보시려면 각 카드 중간의 사이트 이름을 클릭하시면
            원본으로 이동합니다.
          </p>
        </div>
      </div>
    </React.Fragment>
  );
};

export default About;
