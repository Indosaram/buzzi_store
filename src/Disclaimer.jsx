import React from "react";
import { makeStyles } from "@material-ui/core/styles";

const useStyles = makeStyles(() => ({
  disclaimer: {
    margin: "0 10% 0",
  },
  disclaimer__heading: {
    textAlign: "center",
    fontFamily: "paybooc-Bold",
  },
  disclaimer__body: {
    textAlign: "justify",
    fontFamily: "paybooc-Medium",
  },
}));

const Disclaimer = () => {
  const classes = useStyles();
  return (
    <div className={classes.disclaimer}>
    <h1 className={classes.disclaimer__heading}>Disclaimer</h1>
      <p className={classes.disclaimer__body}>
        버찌스토어는 링크, 다운로드 등을 포함하여 본 웹 사이트에 포함되어
        있거나, 본 웹 사이트를 통해 배포, 전송되거나, 본 웹 사이트에 포함되어
        있는 서비스로부터 접근되는 정보(이하 “자료”)의 정확성이나 신뢰성에 대해
        어떠한 보증도 하지 않으며, 서비스상의, 또는 서비스와 관련된 기타 정보
        또는 제안의 결과로서 구매 또는 취득하게 되는 제품 또는 기타 정보(이하
        “제품”)의 질에 대해서도 어떠한 보증도 하지 않습니다.
      </p>
      <p className={classes.disclaimer__body}>
        귀하는, 자료에 대한 신뢰 여부가 전적으로 귀하의 책임임을 인정합니다.
        버찌스토어는 자료 및 서비스의 내용을 수정할 의무를 지지 않으나, 필요에
        따라 개선할 수는 있습니다.
      </p>
      <p className={classes.disclaimer__body}>
        버찌스토어는 자료와 서비스를 “있는 그대로” 제공하며, 서비스 또는 기타
        자료 및 제품과 관련하여 상품성, 특정 목적에의 적합성에 대한 보증을
        포함하되 이에 제한되지 않고 모든 명시적 또는 묵시적인 보증을 명시적으로
        부인합니다.
      </p>
      <p className={classes.disclaimer__body}>
        어떠한 경우에도 버찌스토어는 서비스, 자료 및 제품과 관련하여 직접, 간접,
        부수적, 징벌적, 파생적인 손해에 대해서 책임을 지지 않습니다.
      </p>
      <p className={classes.disclaimer__body}>
        버찌스토어는 본 웹사이트 또는 자료에 열거되어 있는 사이트의 내용을
        검토하려는 노력과 관련하여 어떠한 보증도 하지 않으며 웹사이트 또는
        자료에 열거되어 있는 사이트상의 자료의 정확성, 저작권 준수, 적법성 또는
        도덕성에 대해 아무런 책임을 지지 않습니다.
      </p>
      <p className={classes.disclaimer__body}>
        사이트 이용 시 제휴링크를 통해 일부 수수료를 받을 수 있습니다.
      </p>
    </div>
  );
};

export default Disclaimer;
