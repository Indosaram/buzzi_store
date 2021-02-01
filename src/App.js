import React from "react";
import { Grid } from "@material-ui/core";
import { BrowserRouter, Route, Switch } from "react-router-dom";

import "./App.css";
import Home from "./Home";
import Contact from "./Contact";
import About from "./About";
import Disclaimer from "./Disclaimer";
import Header from "./Header";

class App extends React.Component {
  state = {
    isLoading: true,
    category: "식품/건강",
  };

  getProducts = () => {
    this.setState({ isLoading: false });
  };

  async componentDidMount() {
    this.getProducts();
  }

  onChangeCategory = (value) => {
    this.setState({ category: value });
  };

  render() {
    const { isLoading, category } = this.state;

    return (
      <BrowserRouter>
        <section className="container">
          <Grid
            container
            direction="column"
            className="app"
            style={{ padding: "0 10px 10px" }}
          >
            <Grid item className="app__header">
              <Header
                category={category}
                onChangeValue={this.onChangeCategory}
              />
            </Grid>
            {isLoading ? (
              <div className="loader">
                <span className="loader__text">Loading...</span>
              </div>
            ) : (
              <Switch>
                <Route
                  exact
                  path="/"
                  render={() => <Home category={category} />}
                />
                <Route
                  exact
                  path="/about"
                  render={(props) => <About {...props} />}
                />
                <Route
                  exact
                  path="/contact"
                  render={(props) => <Contact {...props} />}
                />
                <Route
                  exact
                  path="/disclaimer"
                  render={(props) => <Disclaimer {...props} />}
                />
              </Switch>
            )}
          </Grid>
        </section>
      </BrowserRouter>
    );
  }
}

export default App;
