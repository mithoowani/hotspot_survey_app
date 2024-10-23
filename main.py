import streamlit as st
from plotting_functions import *


def hide_streamlit_header_footer():
	hide_streamlit_style = """
                    <style>
                    [data-testid="stToolbar"] {visibility: hidden !important;}
                    footer {visibility: hidden !important;}
                    </style>
                    """
	st.markdown(hide_streamlit_style, unsafe_allow_html=True)


def clean_staff_data(survey_file):
	staff_col_names = ['date',
					   'loc_5west_yn',
					   'loc_8west_yn',
					   'loc_8south_yn',
					   'loc_other_text',
					   'healthcare_discrim',
					   'healthcare_harass',
					   'healthcare_bully',
					   'inclusive',
					   'comments_text']

	# Refers to Excel columns to include
	cols_to_include = 'A:B,H:P'

	Staff = pd.read_excel(survey_file,
						  index_col=0,
						  usecols=cols_to_include)

	Staff.columns = staff_col_names
	Staff.index.name = 'id'
	Staff = Staff.dropna(subset=['date'])  # drops rows with non-submitted surveys

	return Staff


def clean_learner_data(survey_file):
	learner_col_names = ['date',
						 'loc_5west_yn',
						 'loc_8west_yn',
						 'loc_8south_yn',
						 'loc_other_text',
						 'clinical_supported',
						 'clinical_workload',
						 'clinical_comments_text',
						 'healthcare_discrim',
						 'healthcare_harass',
						 'healthcare_bully',
						 'inclusive',
						 'comments_text']

	# Excel columns to include in the dataframe
	cols_to_include = 'A:B,H:S'

	Learner = pd.read_excel(survey_file,
							index_col=0,
							usecols=cols_to_include)

	Learner.columns = learner_col_names
	Learner.index.name = 'id'
	Learner = Learner.dropna(subset=['date'])  # drops rows with non-submitted surveys

	return Learner


def draw_all_charts(_Staff, _Learner, location: str):
	if not _Staff.empty:
		fig = draw_experiences_bar_chart(_Staff, f'STAFF ({location}):')
		st.pyplot(fig)

		fig = draw_inclusive_bar_chart(_Staff, f'STAFF ({location}):')
		st.pyplot(fig)

	if not _Learner.empty:
		fig = draw_experiences_bar_chart(_Learner, f'LEARNERS ({location}):')
		st.pyplot(fig)

		fig = draw_inclusive_and_clinical_bar_chart(_Learner, f'LEARNERS ({location}):')
		st.pyplot(fig)


def main():
	# hide_streamlit_header_footer()
	staff_survey_file = st.file_uploader('Upload STAFF survey Excel file here', type=['xls', 'xlsx'])
	learner_survey_file = st.file_uploader('Upload LEARNER survey Excel file here', type=['xls', 'xlsx'])

	if staff_survey_file and learner_survey_file:
		Staff = clean_staff_data(staff_survey_file)
		Learner = clean_learner_data(learner_survey_file)

		all_ctus, ctu_8s, ctu_8w, ctu_5w = st.tabs(['All CTUs', '8 South', '8 West', '5 West'])

		with all_ctus:
			draw_all_charts(Staff, Learner, 'All CTUs')

		with ctu_8s:
			draw_all_charts(Staff.loc[(Staff['loc_8south_yn'] == 'Yes'), :],
							Learner.loc[(Learner['loc_8south_yn'] == 'Yes'), :],
							'8 SOUTH')

		with ctu_8w:
			draw_all_charts(Staff.loc[(Staff['loc_8west_yn'] == 'Yes'), :],
							Learner.loc[(Learner['loc_8west_yn'] == 'Yes'), :],
							'8 WEST')

		with ctu_5w:
			draw_all_charts(Staff.loc[(Staff['loc_5west_yn'] == 'Yes'), :],
							Learner.loc[(Learner['loc_5west_yn'] == 'Yes'), :],
							'5 WEST')


if __name__ == '__main__':
	main()


# TODO: Comment this file
# TODO: Change names of functions in plotting_functions.py and docstrings