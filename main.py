"""
Streamlit web app for analyzing data from Internal Medicine CTU Hotpsot surveys
Requirements: see requirements.txt, Python 3.10.5
"""

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


def clean_staff_data(survey_file) -> pd.DataFrame:
	"""
	Reads in data from staff survey, renames and drops irrelevant columns and null rows
	:param survey_file: path to staff survey file (xlsx, or xls)
	:return: pandas DataFrame, cleaned staff survey
	"""
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


def clean_learner_data(survey_file) -> pd.DataFrame:
	"""
	Reads in data from learner survey, renames and drops irrelevant columns and null rows
	:param survey_file: path to learner survey file (xlsx, or xls)
	:return: pandas DataFrame, cleaned learner survey
	"""
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


def draw_all_charts(_Staff: pd.DataFrame, _Learner: pd.DataFrame, location: str) -> None:
	"""
	Draws charts from Staff and Learner data sets
	:param _Staff: pd.DataFrame, staff survey results
	:param _Learner: pd.DataFrame, learner survey results
	:param location: string representing location from which data arose
	:return: None
	"""
	if not _Staff.empty:
		experiences_staff_fig = experiences_bar_chart(_Staff, f'STAFF ({location}):')
		st.pyplot(experiences_staff_fig)

		inclusive_fig = inclusive_bar_chart(_Staff, f'STAFF ({location}):')
		st.pyplot(inclusive_fig)

	if not _Learner.empty:
		experiences_learner_fig = experiences_bar_chart(_Learner, f'LEARNERS ({location}):')
		st.pyplot(experiences_learner_fig)

		inclusive_clinical_fig = inclusive_and_clinical_bar_chart(_Learner, f'LEARNERS ({location}):')
		st.pyplot(inclusive_clinical_fig)


def main():
	# hide_streamlit_header_footer()

	# Read in both survey files
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
