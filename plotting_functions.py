import pandas as pd
import numpy as np


def draw_experiences_bar_chart(Survey: pd.DataFrame, title_modifier: str):
	"""
	Draw a bar chart representing experiences of bullying, discrimination and harassment over the last week
	:param Survey: Full survey dataframe
	:param title_modifier: Modifier of the chart title
	:return: None. Draws bar chart.
	"""

	# Prepare data
	exp = Survey.loc[:, ['healthcare_bully', 'healthcare_discrim', 'healthcare_harass']]
	n_responses = len(exp)

	# Convert to category dtype, then Never, Sometimes, Often
	exp = exp.astype('category')
	exp = exp.apply(lambda x: x.cat.set_categories(['Never', 'Sometimes', 'Often']))
	exp_counts = pd.concat([exp.value_counts(col) for col in exp.columns],
						   keys=exp.columns,
						   axis=1)
	exp_counts = exp_counts.transpose()
	exp_counts = exp_counts[['Never', 'Sometimes', 'Often']]
	exp_pct = exp_counts.apply(lambda x: x / x.sum(), axis=1)  # normalized

	# Draw stacked bar chart
	colors = ['tab:green', 'tab:orange', 'tab:red']
	ax = exp_pct.plot.bar(stacked=True, color=colors)

	ax.set_yticks(np.linspace(0, 1, 11))
	ax.set_yticklabels((ax.get_yticks() * 100).astype('int64'))
	ax.set_xticklabels(['Bullying', 'Discrimination', 'Harassment'])

	ax.grid(axis='y')  # Only horizontal grid lines
	ax.legend(title=f'Responses (n={n_responses})',
			  loc=(1.05, 0.5))

	chart_title = title_modifier + ' ' + 'Frequency of bullying, discrimination, and harassment \nfrom members of the healthcare team over the last week'

	ax.set_title(chart_title, fontsize=15)
	ax.set_ylabel('Percentage', fontsize=15)

	return ax.get_figure()


def draw_inclusive_bar_chart(Survey: pd.DataFrame, title_modifier: str):
	"""
	Draw a bar chart representing feelings of inclusiveness over the last week
	:param Survey: Full survey dataframe
	:param title_modifier: Modifier of the chart title
	:return: None. Draws bar chart.
	"""

	# Prepare data
	inclusive = Survey['inclusive'].astype('category')
	inclusive = inclusive.cat.set_categories(['Always', 'Often', 'Sometimes', 'Never'])
	incl_counts = inclusive.value_counts(normalize=True, sort=False) * 100  # Normalized
	n_responses = len(inclusive)

	# Bar chart for inclusive work environment
	ax = incl_counts.plot.bar(
		incl_counts,
		color=['tab:green', 'tab:olive', 'tab:orange', 'tab:red'],
		stacked=True)

	chart_title = title_modifier + ' ' + f'The work environment feels inclusive (n={n_responses})'

	ax.set_title(chart_title, fontsize=15)
	ax.set_ylabel('Percentage', fontsize=15)
	ax.grid(axis='y')
	ax.set_xlabel('')

	return ax.get_figure()


def draw_inclusive_and_clinical_bar_chart(Survey: pd.DataFrame, title_modifier: str):
	"""
	Draw a bar chart representing experience of clinical work and inclusiveness over the last week
	:param Survey: Full survey dataframe
	:param title_modifier: Modifier of the chart title
	:return: None. Draws bar chart.
	"""

	# Prepare data
	exp = Survey.loc[:, ['clinical_supported', 'clinical_workload', 'inclusive']]
	n_responses = len(exp)

	# Convert to category dtype, then Never, Sometimes, Often, Always
	exp = exp.astype('category')
	exp = exp.apply(lambda x: x.cat.set_categories(['Always', 'Often', 'Sometimes', 'Never']))
	exp_counts = pd.concat([exp.value_counts(col) for col in exp.columns],
						   keys=exp.columns,
						   axis=1)
	exp_counts = exp_counts.transpose()
	exp_counts = exp_counts[['Always', 'Often', 'Sometimes', 'Never']]  # ensures the proper order is preserved
	exp_pct = exp_counts.apply(lambda x: x / x.sum(), axis=1)  # normalized

	# Draw stacked bar chart
	colors = ['tab:green', 'tab:olive', 'tab:orange', 'tab:red']
	ax = exp_pct.plot.bar(stacked=True, color=colors)

	ax.set_yticks(np.linspace(0, 1, 11))
	ax.set_yticklabels((ax.get_yticks() * 100).astype('int64'))
	ax.set_xticklabels(['Felt supported by \n supervisor/senior resident',
						'Clinical workload \n was manageable',
						'Work environment \n is inclusive'])

	ax.grid(axis='y')  # Only horizontal grid lines
	ax.legend(title=f'Responses (n={n_responses})',
			  loc=(1.05, 0.5))

	chart_title = title_modifier + ' ' + 'Experiences of clinical work and learning environment'

	ax.set_title(chart_title, fontsize=15)

	ax.set_ylabel('Percentage', fontsize=15)

	return ax.get_figure()
