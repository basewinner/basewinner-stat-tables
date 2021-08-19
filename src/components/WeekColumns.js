import { format } from 'date-fns'

export const WEEK_COLUMNS = [

  {
    Header: 'Name',
    Footer: 'Name',
    accessor: 'name',
    className: 'left'
      
  },
  {
    Header: 'Team',
    Footer: 'Team',
    accessor: 'team'
  },
  {
    Header: 'Week Ending',
    Footer: 'Week Ending',
    accessor: 'week',
  },
  {
    Header: 'PA',
    Footer: 'PA',
    accessor: 'pa',
    disableFilters: true
  },
  {
    Header: 'BaseRuns9',
    Footer: 'BaseRuns9',
    accessor: 'base_runs_p9',
    disableFilters: true
  },
  {
    Header: 'BRpct',
    Footer: 'BRpct',
    accessor: 'br9_rank',
    disableFilters: true,
  },
  {
    Header: 'HH9',
    Footer: 'HH9',
    accessor: 'hh9',
    disableFilters: true,
    Cell: ({ value }) => {
      return format(value, value.toFixed(1))
    }
  },
  {
    Header: 'HH9pct',
    Footer: 'HH9pct',
    accessor: 'hh9_rank',
    disableFilters: true
  },
  {
    Header: 'xBB%',
    Footer: 'xBB%',
    accessor: 'xwr',
    disableFilters: true,
    Cell: ({ value }) => {
      return format(value, value.toFixed(3))
    }
    
  },
  {
    Header: 'xK%',
    Footer: 'xK%',
    accessor: 'expected_k_pct',
    disableFilters: true
  },
  {
    Header: 'xBB/K',
    Footer: 'xBB/K',
    accessor: 'xbbk',
    disableFilters: true,
},
 {
    Header: 'xBB/Kpct',
    Footer: 'xBB/Kpct',
    accessor:'xbbk_rank',
    disableFilters: true,
    
  },
  {
    Header: 'BW PCT',
    Footer: 'BW PCT',
    accessor: '3M Batting Pct',
    disableFilters: true
},
 {
    Header: 'Rank',
    Footer: 'Rank',
    accessor: '3M Batting Rank',
    disableFilters: true
  },
]
