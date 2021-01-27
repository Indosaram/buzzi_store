import React from "react";
import { AppBar, Toolbar } from "@material-ui/core";
import { makeStyles } from "@material-ui/core/styles";
import buzziLogo from "./buzzi-store-logo.png";

const useStyles = makeStyles((theme) => ({
  header: {
    backgroundColor: "white",
    height: 50,
    boxShadow: "None",
  },
  header__toolbar: {
    padding: 0,
  },
  logo: {
    maxWidth: 120,
  },
}));

const Header = () => {
  const classes = useStyles();
  return (
    <React.Fragment>
      <AppBar
        id="back-to-top-anchor"
        className={classes.header}
        position="static"
      >
        <Toolbar className={classes.header__toolbar}>
          <a href="/">
            <img
              className={classes.logo}
              src={buzziLogo}
              alt="Buzzi store logo"
            />
          </a>
        </Toolbar>
      </AppBar>
    </React.Fragment>
  );
};

export default Header;
