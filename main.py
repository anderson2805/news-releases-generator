import streamlit as st
import pandas as pd
from src.loader import load_nrs
from src.semantic_search import get_similar_score, get_embeddings, get_similar_indices
from st_aggrid import AgGrid, GridOptionsBuilder, JsCode, ColumnsAutoSizeMode
from src.generate import create_prompt_info, create_prompt_report
from src.chat import get_chat_response
nrs_repository = load_nrs()

st.set_page_config(
    layout="wide",
    page_title="NR-GPT",
    page_icon="📃",
)


if "grid_key" not in st.session_state:
    st.session_state.grid_key = 0

st.header("NR-GPT 📃")
st.markdown("""To generate draft news release reports, we will search for the most relevant news releases to use as templates based on the title of the news release. GPT will learn from the style of the related news releases and determine which information needs to be included in the report.

Once the user provides the necessary information, GPT will generate a draft news release.
""")

seed_title = st.text_input('Enter a title of the news release you are working on:', key = 'seed_title', value=st.session_state.get('seed_title', ''))
st.button('Search', key='search')

if (st.session_state.get('search')):
    st.session_state.grid_key += 1

    seed_title_embedding = get_embeddings(st.session_state.seed_title)

    similar_indices = get_similar_indices(seed_title_embedding, top_n = 3)

    nrs_repository_df = pd.DataFrame(nrs_repository)

    nrs_repository_df['date'] = pd.to_datetime(nrs_repository_df['date'], format='%d %b %Y %H:%M (GMT+8)')

    nrs_repository_df['Related%'] = get_similar_score(seed_title_embedding)
    # Change column Related to 1f
    nrs_repository_df['Related%'] = nrs_repository_df['Related%'].apply(lambda x: f'{x:.1f}')
    # Change column Related to int
    nrs_repository_df['Related%'] = nrs_repository_df['Related%'].astype(float)

    # Replace type Military Recognition and Awards to Military Recognition & Awards
    nrs_repository_df['type'] = nrs_repository_df['type'].replace('Military Recognition and Awards', 'Military Recognition & Awards')

    nrs_repository_df['selected'] = ''

    nrs_repository_df.sort_values(by='Related%', ascending=False, inplace= True)
    st.session_state.nrs_repository_df = nrs_repository_df
    

# If st.session_state contain nrs_repository_df
if type(st.session_state.get('nrs_repository_df', False))==pd.DataFrame:
    col1, col2 = st.columns([2,1])
    nrs_repository_df = st.session_state.get('nrs_repository_df', pd.DataFrame())
    with col1:
        BtnCellRenderer = JsCode('''
        class BtnCellRenderer {
            init(params) {
                this.params = params;
                this.eGui = document.createElement('div');
                this.eGui.innerHTML = `
                <span>
                    <button id='click-button' 
                        class='btn-simple' 
                        style='color: ${this.params.color}; background-color: ${this.params.background_color}'>View Article</button>
                </span>
            `;

                this.eButton = this.eGui.querySelector('#click-button');
                this.btnClickedHandler = this.btnClickedHandler.bind(this);
                this.eButton.addEventListener('click', this.btnClickedHandler);

            }

            getGui() {
                return this.eGui;
            }

            refresh() {
                return true;
            }

            destroy() {
                if (this.eButton) {
                    this.eGui.removeEventListener('click', this.btnClickedHandler);
                }
            }

            btnClickedHandler(event) {
                this.refreshTable(new Date().toLocaleString());
                console.log(this.params);
                console.log(this.params.getValue());
            }


            refreshTable(value) {
                this.params.setValue(value);
            }
        };
        ''')
        # JsCode that return index of selected rows
        st.write('Select Relevant News Releases (Max 3 selections):')
        
        # All indicies in integer
        gb = GridOptionsBuilder.from_dataframe(nrs_repository_df[['date', 'title', 'type', 'Related%']])
        gb.configure_pagination(enabled= True, paginationAutoPageSize=False, paginationPageSize=15)
        gb.configure_grid_options(domLayout='normal')
        gb.configure_selection('multiple', use_checkbox=True)
        gb.configure_auto_height(True)
        
        gridOptions = gb.build()
        gridOptions['columnDefs'].append({
            "field": "selected",
            "header": "Selected",
            "cellRenderer": BtnCellRenderer,
            "cellRendererParams": {
                "color": "white",
                "background_color": "grey",
            },
        })
        grid_response = AgGrid(
            nrs_repository_df, gridOptions, columns_auto_size_mode=ColumnsAutoSizeMode(2), update_on=['selectionChanged','rowClicked'], enable_enterprise_modules=True, allow_unsafe_jscode=True, reload_data=False, key= f'grid{st.session_state.grid_key}')
        
    with col2:
        try:
            st.session_state['view_details'] = grid_response['data'][grid_response['data']['selected'] != ''].sort_values(by='selected', ascending=False).head(1)
            article_selected = st.session_state['view_details']['article'].values[0].replace('\n', '\n\n')
            url_selected = st.session_state['view_details']['url'].values[0]
            article_content = st.text_area('NR content:', height=500, key='selected_nr_content', disabled = False, value=article_selected)
            st.write('URL:', url_selected)
        except:
            article = []

    st.markdown('---')
    if st.session_state.get('prev_selection', 0) != len(grid_response.selected_rows):
        st.session_state['prompt1'] = create_prompt_info(seed_title, grid_response.selected_rows)

    st.session_state['prev_selection'] = len(grid_response.selected_rows)
    
    with st.form("form_1"):
        prompt1 = st.text_area('Prompt 1: To get information needed to generate the NR.', height=500, key='prompt1', disabled = False)
        send1_1, blank1, send1_2 = st.columns([5,1,1])
        with send1_2:
            send1 = st.form_submit_button('Analyze Related News Releases')
        if send1:
            with st.spinner('Calling ChatGPT... seeking information needed to generate report...'):
                st.session_state['info_required'] = get_chat_response(prompt1)
                st.session_state['prompt2'] = create_prompt_report(seed_title, st.session_state['info_required'], grid_response.selected_rows)

    with st.form("form_2"):
        if send1 or st.session_state.get('prompt2', False) or st.session_state.get('send2_save', False):
            prompt2 = st.text_area('Prompt 2: Add information to generate the NR.', height=500, key='prompt2', disabled = False)
            send2_1, blank2, send2_2 = st.columns([5,1,1])
            with send2_2:
                st.write('\n \n ')
                send2 = st.form_submit_button('Generate Draft Report', use_container_width=True)
            with send2_1:
                st.slider('Temperature', min_value=0.0, max_value=2.0, value=0.0, step=0.1, key='temperature')
            if send2:
                st.session_state['send2_save'] = True
                with st.spinner('Calling ChatGPT... Generating report...'):
                    st.session_state['draft_report'] = get_chat_response(prompt2, st.session_state.temperature)
            if st.session_state.get('draft_report'):
                st.text_area('Draft Report:', height=500, key='draft_report', disabled = False)