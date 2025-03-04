import streamlit as st
from functions_constants import donnes_techniques_dict, find_valid_xml, categories

import zipfile
import xml.etree.ElementTree as ET
import os
import io  # To store XML in memory before writing to ZIP
import pandas as pd

import datetime


# Example predefined values extracted from XML
predefined_values = {
    "type_structure_principale": "2",  # Meaning "Poteaux/poutres"
    "elements_prefabriques": "1",  # Meaning "oui"
    "materiau_structure": "6"  # Meaning "Béton haute performance"
}

# Your dictionary with options
# data_dict = donnes_techniques_dict




# --- FILE UPLOAD ------------------------------------------------------------------------------
uploaded_file = st.file_uploader("Choose a ZIP file", type=["zip"])

if uploaded_file:
    # Save file temporarily
    temp_dir = "temp_dir"
    temp_path = os.path.join(temp_dir, uploaded_file.name)
    os.makedirs(temp_dir, exist_ok=True)
    
    # st.write(temp_path)
    # st.write("yuyuyuyuyu")
    # if "zip_path" in st.session_state:
    #     st.write(st.session_state["zip_path"])    
    
    base_name, ext = os.path.splitext(temp_path)

    testing_file_path = f"{base_name}_KIC{ext}"
    # st.write(testing_file_path)





    # # When a new file is uploaded, reset session state variables
    if "zip_path" in st.session_state and st.session_state["zip_path"] != testing_file_path:
        del st.session_state["zip_path"]  # Remove old file reference

    with open(temp_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    # Initialize session state for zip tracking
    if "zip_path" not in st.session_state:
        st.session_state["zip_path"] = temp_path  # Track the latest ZIP version
        


   # --- ZIP EXTRACTION CHECK ---
    try:
        with zipfile.ZipFile(temp_path, "r") as zip_ref:
            file_list = zip_ref.namelist()
            # st.write(file_list)
        
        st.success(f"✅ File **<{uploaded_file.name}>** uploaded and verified successfully! Number of XML Files: **{len([f for f in file_list if f.endswith('.xml')])}**")
        # st.write(temp_path)

    except zipfile.BadZipFile:
        st.error("❌ Invalid ZIP file. Please upload a valid ZIP archive.")

    uploaded_file_name = uploaded_file.name
    zip_path = temp_path
    
# --- FILE UPLOAD ------------------------------------------------------------------------------

    if "zip_path" in st.session_state:
        # st.write("yuyuyuyuyu")

        # st.write(st.session_state["zip_path"])

    #------------------------------------------getting batiments names for selectboxes ----------------------------------------
        with zipfile.ZipFile(st.session_state["zip_path"], 'r') as zip_ref:
            files_list = zip_ref.namelist() #get all files inside zip
            # st.write(files_list)

            file_name = os.path.basename(st.session_state["zip_path"])
            #debugging
            # st.write(f"Files inside the zip **{file_name}**")
            # for file in files_list:
            #     st.write(f"   -   {file}")
            #debugging

            xml_files = [f for f in files_list if f.endswith(".xml")]
            # st.write(f"\nXML files found : {xml_files}")


            # st.write(xml_files)

            xml_ = find_valid_xml(xml_files) #if there are not fiches configures the folder structure changes so the find_valid_function doenst work anymore
            # st.write(xml_)

            # if xml_ is None :
            #     xml_ = xml_files[0]

            # print(f'The xml file to get the batiment names is {xml_}')

            with zip_ref.open(xml_) as file:
                tree = ET.parse(file)
                root = tree.getroot()

                if root.tag == "projet":
                    print("This is a RSEE")
                    batiments_rsenv = root.findall(".//RSEnv/entree_projet/batiment")
                    all_buildings = []

                    for batiment in batiments_rsenv:
                        batiment_nom = batiment.find("nom").text
                        # batiment_index = batiment.find("index").text
                        all_buildings.append(batiment_nom)
        
        # st.write(all_buildings)
        # 🚨 If no building is selected, show an error and stop execution

    #------------------------------------------getting batiments names for selectboxes ----------------------------------------


    # --- MULTISELECT WITH DEFAULT VALUES for batiments names ------------------------------------------------------------------------------------------------------
        selected_buildings = st.multiselect(
            "Choose Buildings:", options=all_buildings, default=all_buildings
        )

        # st.write(selected_buildings)
        if not selected_buildings:
            st.warning("⚠️ Please select at least one building to proceed.")
            st.stop()  # 🛑 Stops execution here, preventing further errors


    # --- MULTISELECT WITH DEFAULT VALUES for batiments names---------------------------------------------------------------------------------------



        
    # ---------------------------- Read xml, filter buildings, and get its current donnees techniques ------------------------------------------------------------------

        with zipfile.ZipFile(st.session_state["zip_path"], 'r') as zip_ref:
            files_list = zip_ref.namelist() #get all files inside zip

            #debugging
            # print("Files inside the zip")
            # for file in files_list:
            #     print(f"   -   {file}")
            #debugging

            xml_files = [f for f in files_list if f.endswith(".xml")]
            # print(f"\nXML files found : {xml_files}")


            # st.write("xml_files 01")

            xml_ = find_valid_xml(xml_files) #if there are not fiches configures the folder structure changes so the find_valid_function doenst work anymore
            # st.write(xml_)
            # if xml_ is None :
            #     xml_ = xml_files[0]

            print(f'The xml file to get default donnes generales is {xml_}')

            with zip_ref.open(xml_) as file:
                tree = ET.parse(file)
                root = tree.getroot()

                if root.tag == "projet":
                    print("This is a RSEE")
                    batiments_rsenv = root.findall(".//RSEnv/entree_projet/batiment")
                    choiced_batiments = []
                    data_dict = {}

                    for batiment in batiments_rsenv:
                        batiment_nom = batiment.find("nom").text

                        if batiment_nom in selected_buildings:
                            batiment_index = batiment.find("index").text
                            print(f"Selected batiment: {batiment_nom} (Index: {batiment_index})")
                            choiced_batiments.append(batiment_index)

                    print(f"\n📌 Selected batiments: {choiced_batiments}")

                    batiments_datas_comp = root.findall(".//Datas_Comp/batiment_collection/batiment")
                    print(f"\nFound {len(batiments_datas_comp)} batiments in Datas_comp")


                    for batiment_dc in batiments_datas_comp :
                        batiment_dc_index = batiment_dc.find("Index").text

                        if batiment_dc_index in choiced_batiments:
                            print(f"\nProcessing batiment with index {batiment_dc_index}")

                            donnees_techniques = batiment_dc.find("donnees_techniques")

                            data_dict[batiment_dc_index] = {}

                            for parametre in donnees_techniques:
                                key = parametre.tag
                                value = parametre.text
                                data_dict[batiment_dc_index][key] = value


    # ---------------------------- Read xml, filter buildings, and get its current donnees techniques ------------------------------------------------------------------



    # ---------------------#### We then compare the donnes techniques among the buildings and we get the current state of donnes techniques ---------------------------

        keys_ = next(iter(data_dict.values()))
        common_keys = set(keys_.keys())
        final_dict = {}

        for key in common_keys:
            values_set = set()

            for batiment_id, batiment_data in data_dict.items():
                value = batiment_data[key]
                values_set.add(value)
            
            if len(values_set) == 1:
                final_dict[key] = values_set.pop()
            else:
                final_dict[key] = "000"
            
        # st.write(final_dict)
        predefined_values = final_dict

    # ---------------------#### We then compare the donnes techniques among the buildings and we get the current state of donnes techniques ---------------------------
        
    
    # Iterate through each category ------------------------------------------------------------------
        # Store user selections
        selected_options = {}

        for category_name, fields in categories.items():
            with st.expander(f"{category_name}"):  # Collapsible sections
                cols = st.columns(2)  # Arrange into 2 columns for better readability
                
                for i, field in enumerate(fields):
                    col = cols[i % 2]  # Distribute evenly between columns
                    # st.write(field)
                    options = donnes_techniques_dict[field]  # Get available choices
                    reversed_options = {v: k for k, v in options.items()}  # Reverse mapping
                    
                    # Get predefined value, fallback to first
                    predefined_key = predefined_values.get(field, None)
                    predefined_label = options.get(predefined_key, list(options.values())[0])

                    if predefined_key == "000":
                        col.warning(f"🔽 **{field.replace('_', ' ').capitalize()}** values are not equal among batiments. Set as défault")
                        # Select box
                        selected_value = col.selectbox(
                            f"{field.replace('_', ' ').capitalize()}",
                            list(reversed_options.keys()),
                            index=list(reversed_options.keys()).index(predefined_label)
                        )

                    else:
                        # Select box
                        selected_value = col.selectbox(
                            f"{field.replace('_', ' ').capitalize()}",
                            list(reversed_options.keys()),
                            index=list(reversed_options.keys()).index(predefined_label)
                        )

                    # Store selection
                    selected_options[field] = reversed_options[selected_value]
        
        # st.write(selected_options)

    # Iterate through each category ------------------------------------------------------------------

        st.success("✅ Sélections enregistrées avec succès !")



    # -------------------------------------- from user input modify and save new zip and download button -------------------------------------------------------
    # Process and modify the XML inside the ZIP
        # zip_path = temp_path  # Replace with the actual path where the uploaded zip is stored


        base_name, ext = os.path.splitext(uploaded_file_name)
        current_date = datetime.datetime.now().strftime("%d%m%Y")

        modified_file_name = f"{base_name}_KIC_{current_date}{ext}"
        

        new_zip_path = os.path.join(temp_dir, f"{base_name}_KIC{ext}")
        # st.write(modified_file_name)
        # st.write(base_name)
        # st.write(new_zip_path)

        if "counter" not in st.session_state:
            st.session_state['counter'] = 0

        # Button to **Apply Changes** to the ZIP file
        if st.button("🛠️ Apply Changes to ZIP"):

                        # st.write(selected_buildings)
            if st.session_state['counter'] == 1:
                st.warning("⚠️ We are tired we cant change more data, please refresh the page and try again")
                st.info("**Tip**: If you want to change another group of buildings re upload the downloaded zip and change only that group")
                st.stop()  # 🛑 Stops execution here, preventing further errors
            st.session_state['counter'] += 1

            with zipfile.ZipFile(st.session_state["zip_path"], 'r') as zip_ref:
                files_list = zip_ref.namelist()
                xml_files = [f for f in files_list if f.endswith(".xml")]

                st.write(st.session_state['counter'])
                st.write("xml_files_03")
                xml_ = find_valid_xml(xml_files)  # Custom function to select XML
                if xml_ is None:
                    xml_ = xml_files[0]


                # st.write(new_zip_path)
                with zipfile.ZipFile(new_zip_path, 'w') as new_zip:
                    # st.write(xml_)
                    with zip_ref.open(xml_) as file:
                        tree = ET.parse(file)
                        root = tree.getroot()

                        if root.tag == "projet":
                            batiments_rsenv = root.findall(".//RSEnv/entree_projet/batiment")
                            choiced_batiments = []

                            for batiment in batiments_rsenv:
                                batiment_nom = batiment.find("nom").text
                                if batiment_nom in selected_buildings:
                                    batiment_index = batiment.find("index").text
                                    choiced_batiments.append(batiment_index)

                            batiments_datas_comp = root.findall(".//Datas_Comp/batiment_collection/batiment")

                            for batiment_dc in batiments_datas_comp:
                                batiment_dc_index = batiment_dc.find("Index").text
                                if batiment_dc_index in choiced_batiments:
                                    donnees_techniques = batiment_dc.find("donnees_techniques")
                                    for elements in donnees_techniques:
                                        element_key = elements.tag
                                        element_value = elements.text
                                        if element_key in selected_options:  # Update only if in selected options
                                            new_element_value = selected_options[element_key]
                                            elements.text = new_element_value

                            # Remove extra xmlns
                            for elem in root.iter():
                                if 'xmlns' in elem.attrib:
                                    del elem.attrib['xmlns']

                            # Save modified XML
                            modified_xml_bytes = io.BytesIO()
                            tree.write(modified_xml_bytes, encoding="utf-8", xml_declaration=False)
                            modified_xml_str = modified_xml_bytes.getvalue().decode("utf-8")

                            if not modified_xml_str.startswith("<?xml"):
                                modified_xml_str = '<?xml version="1.0" encoding="utf-8"?>\n' + modified_xml_str

                            new_zip.writestr(xml_, modified_xml_str.encode("utf-8"))

                    # Copy unmodified files
                    for file_name in zip_ref.namelist():
                        if file_name != xml_:
                            with zip_ref.open(file_name) as original_file:
                                new_zip.writestr(file_name, original_file.read())


            # ✅ Update the session state to point to the latest modified ZIP
            
            # st.write("bobobobobo")
            # st.write(st.session_state["zip_path"])
            # st.write(new_zip_path)
            # st.write("bobobobobo")
            st.session_state["zip_path"] = new_zip_path  # <------ UPDATED HERE!

            st.success("✅ Changes Applied! Donnees Techniques updated.")

            # Store flag to enable download
            st.session_state["new_zip_ready"] = True  

        # st.write("bobobobobo")
        # st.write(st.session_state["zip_path"])
        # st.write(new_zip_path)
        # st.write("bobobobobo")
        # Only show the download button if changes have been applied

        if "new_zip_ready" in st.session_state and st.session_state["new_zip_ready"]:
            with open(new_zip_path, "rb") as f:
                zip_bytes = f.read()

            st.download_button(
                label="📥 Download Modified ZIP",
                data=zip_bytes,
                file_name=modified_file_name,
                mime="application/zip"
            )

        # st.write(selected_options)
    # -------------------------------------- from user input modify and save new zip and download button -------------------------------------------------------























    # # Iterate through each category (top-level key)
    # for category, options in data_dict.items():
    #     # Reverse the dictionary: {label: key}
    #     reversed_options = {v: k for k, v in options.items()}
        
    #     # Retrieve predefined value, default to the first item if missing
    #     predefined_key = predefined_values.get(category, None)  # Get key ("2", "1", etc.)
    #     predefined_label = options.get(predefined_key, list(options.values())[0])  # Convert key to label
        
    #     # Create the selectbox with the predefined value as default
    #     selected_value = st.selectbox(
    #         f"Choisissez une option pour {category.replace('_', ' ')}:",
    #         list(reversed_options.keys()),  # Show readable options
    #         index=list(reversed_options.keys()).index(predefined_label)  # Preselect the predefined value
    #     )

    #     # Store the selected numerical key in the dictionary
    #     selected_options[category] = reversed_options[selected_value]

    # Display the final dictionary with selected keys

