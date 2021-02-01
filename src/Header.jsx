import React from "react";
import { Link } from "react-router-dom";
import PropTypes from "prop-types";

import { AppBar, Toolbar } from "@material-ui/core";
import { makeStyles } from "@material-ui/core/styles";
import IconButton from "@material-ui/core/IconButton";
import Drawer from "@material-ui/core/Drawer";
import List from "@material-ui/core/List";
import Divider from "@material-ui/core/Divider";
import ListItem from "@material-ui/core/ListItem";
import ListItemIcon from "@material-ui/core/ListItemIcon";
import ListItemText from "@material-ui/core/ListItemText";
import InfoIcon from "@material-ui/icons/Info";
import MailIcon from "@material-ui/icons/Mail";
import HomeIcon from "@material-ui/icons/Home";
import MenuIcon from "@material-ui/icons/Menu";
import NewReleasesIcon from "@material-ui/icons/NewReleases";

import buzziLogo from "./buzzi-store-logo.png";
import CategoryListMenu from "./Category";

const useStyles = makeStyles((theme) => ({
  root: {
    flexGrow: 1,
  },
  header: {
    backgroundColor: "white",
    height: 60,
    boxShadow: "None",
  },
  header__toolbar: {
    padding: 0,
  },
  logo: {
    maxWidth: 120,
  },
  header__menuButton: {
    color: "#FE6B8B",
  },
  header__category: {},
  list: {
    width: 250,
  },
  icon: {
    color: "#FE6B8B",
  },
  link: {
    color: "black",
    textDecoration: "none",
  },
}));

const Header = ({ category, onChangeValue }) => {
  const classes = useStyles();
  const [state, setState] = React.useState({
    left: false,
  });


  const toggleDrawer = (open) => (event) => {
    if (
      event.type === "keydown" &&
      (event.key === "Tab" || event.key === "Shift")
    ) {
      return;
    }

    setState({ ...state, left: open });
  };

  const list = (
    <div
      className={classes.list}
      role="presentation"
      onClick={toggleDrawer(false)}
      onKeyDown={toggleDrawer(false)}
    >
      <List>
        <Link to="/" className={classes.link}>
          <ListItem button key={"Home"}>
            <ListItemIcon>
              <HomeIcon className={classes.icon} />
            </ListItemIcon>
            <ListItemText primary={"Home"} />
          </ListItem>
        </Link>
      </List>
      <Divider />
      <List>
        <Link to="/about" className={classes.link}>
          <ListItem button key={"About"}>
            <ListItemIcon>
              <InfoIcon className={classes.icon} />
            </ListItemIcon>
            <ListItemText primary={"About"} />
          </ListItem>
        </Link>
        <Link to="/contact" className={classes.link}>
          <ListItem button key={"Contact"}>
            <ListItemIcon>
              <MailIcon className={classes.icon} />
            </ListItemIcon>
            <ListItemText primary={"Contact"} />
          </ListItem>
        </Link>
        <Link to="/disclaimer" className={classes.link}>
          <ListItem button key={"Disclaimer"}>
            <ListItemIcon>
              <NewReleasesIcon className={classes.icon} />
            </ListItemIcon>
            <ListItemText primary={"Disclaimer"} />
          </ListItem>
        </Link>
      </List>
    </div>
  );

  return (
    <React.Fragment>
      <div className={classes.root}>
        <AppBar
          id="back-to-top-anchor"
          className={classes.header}
          position="static"
        >
          <Toolbar className={classes.header__toolbar}>
            <IconButton
              edge="start"
              className={classes.header__menuButton}
              aria-label="menu"
              onClick={toggleDrawer(true)}
            >
              <MenuIcon />
            </IconButton>
            <Drawer
              anchor="left"
              open={state["left"]}
              onClose={toggleDrawer(false)}
            >
              {list}
            </Drawer>
            <a href="/">
              <img
                className={classes.logo}
                src={buzziLogo}
                alt="Buzzi store logo"
              />
            </a>
            <CategoryListMenu
              set_category={category}
              onChange={onChangeValue}
              className={classes.header__category}
            />
          </Toolbar>
        </AppBar>
      </div>
    </React.Fragment>
  );
};

Header.propTypes = {
  category: PropTypes.string.isRequired,
};

export default Header;
