import React from "react";
import PropTypes from "prop-types";
import { makeStyles } from "@material-ui/core/styles";
import MenuItem from "@material-ui/core/MenuItem";
import FormControl from "@material-ui/core/FormControl";
import Select from "@material-ui/core/Select";
import { Typography } from "@material-ui/core";

const options = [
  "전체보기",
  "기타",
  "컴퓨터",
  "게임/디지털",
  "식품/건강",
  "서적",
  "가전/가구",
  "육아",
  "상품권",
  "화장품",
  "의류/잡화",
  "인테리어",
  "취미/레저",
];

const useStyles = makeStyles((theme) => ({
  formControl: {
    margin: theme.spacing(1),
    minWidth: 120,
  },
  formControl__text: {
    fontFamily: "paybooc-Medium",
  },
}));

export default function CategoryListMenu({ set_category, onChange }) {
  const classes = useStyles();
  const [category, setAge] = React.useState(set_category);
  const [open, setOpen] = React.useState(false);

  const handleChange = (event) => {
    setAge(event.target.value);
    onChange(event.target.value);
  };

  const handleClose = () => {
    setOpen(false);
  };

  const handleOpen = () => {
    setOpen(true);
  };

  return (
    <div>
      <FormControl className={classes.formControl}>
        <Select
          labelId="demo-controlled-open-select-label"
          id="demo-controlled-open-select"
          open={open}
          onClose={handleClose}
          onOpen={handleOpen}
          value={category}
          onChange={handleChange}
        >
          {options.map((option, index) => {
            return (
              <MenuItem key={index} value={option}>
                <Typography className={classes.formControl__text}>
                  {option}
                </Typography>
              </MenuItem>
            );
          })}
        </Select>
      </FormControl>
    </div>
  );
}

CategoryListMenu.propTypes = {
  set_category: PropTypes.string.isRequired,
};
