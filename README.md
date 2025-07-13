# 📚 **README**

## 🐍 Project: Form Builder with Python 3.12 and Tkinter

A simple and flexible tool for creating custom forms and managing a database, built with **Python 3.12** and the **Tkinter** library.

---

## ✅ Project Structure

To use this project, you need **2 empty modules**:

| File Name                  | Description                                                                                                                                                                                     |
| -------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **`ejmin_db.py`**          | This empty module is used to store the database structure. All tables and related structures will be generated here.                                                                            |
| **`<your_name>_ejmin.py`** | This module must end with **`_ejmin.py`**. Inside it, you only need to import `form_db.py`. Running this file will open the form where you define how your form and database should be created. |

---

## ⚙️ How to Run

1. Required files:

   * `form_db.py` → The main project module (do not modify)
   * `ejmin_db.py` → Empty (for the database structure)
   * `<your_name>_ejmin.py` → Empty (only for running)

2. In `<your_name>_ejmin.py` add:

   ```python
   import form_db
   ```

3. Run `<your_name>_ejmin.py` to open the form.

---

## 🧩 How the Form and Database Are Created

✅ **Title/Description:**
Add a text description or title for your form.

✅ **Labels + Entry Fields:**
Each label comes with an `Entry` field. Each label will become a field in the database.
Format:

```
a_texty_name|str
a_integery_age|int
```

✅ **Buttons with Entry Fields:**
You can add buttons that have an `Entry` field next to them. Just provide the button name.

✅ **Standalone Buttons:**
You can add buttons without an `Entry` field.
The number of standalone buttons must be:

* Exactly 1, or
* Even, or
* A multiple of 3.

✅ **Checkbox for Listbox:**
You can choose whether your form should include a `Listbox`.

✅ **Table/Class Name for Database:**

* Define the table name.
* The table fields are created exactly based on the labels and their data types.
* If the table name already exists, an error message will appear.

---

## ⚠️ Input Validation

After filling out the form, click the `Create` button:

* It will check that:

  * Field names are not duplicated.
  * Button names do not conflict with Python built-in keywords (since each button name will be used to define a function).
  * Data types (`str` or `int`) are correctly specified.
  * The table name has not been used before.

If there is an issue, an appropriate error message will be shown.

---

## 🗃️ Database Structure

* Once validated, the form and database are automatically created based on your input.
* Each table includes the following methods:

  * `validate`, `create`, `update`, `delete`, `read`, `get_score`
* The `read`, `delete`, `get_score`, and `validate` methods are defined in a parent class for easy inheritance by other tables.
* **The `read` method**:

  * Can return all records in the table.
  * Can perform advanced searches on any number of fields you specify.
  * Supports wildcard operators like `*` and `?` for more flexible queries.

---

## 🔗 Summary

✅ `form_db.py` → Main module
✅ `ejmin_db.py` → Empty module for the database structure
✅ `<your_name>_ejmin.py` → Empty; just import `form_db` and run it
✅ The form and database will be created exactly according to your configuration. 🚀

