import { format } from 'date-fns'
import { basic }from './sortTypes'
import './WeekTable.css'

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
    disableFilters: true,
    Cell: ({ value }) => {
      return format(value, value.toFixed(1))
    }
  },
  {
    Header: 'BRpct',
    Footer: 'BRpct',
    accessor: 'br9_rank',
    sortType: basic,
    disableFilters: true,
    Cell: ({ value }) => {
      return format(value, value.toFixed(3))
    }
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
    disableFilters: true,
    sortType: basic,
    Cell: ({ value }) => {
      return format(value, value.toFixed(3))
    }
  },
  {
    Header: 'xBB%',
    Footer: 'xBB%',
    accessor: 'xwr',
    disableFilters: true,
    sortType: basic,
    Cell: ({ value }) => {
      return format(value, value.toFixed(2))
    }
    
  },
  {
    Header: 'xK%',
    Footer: 'xK%',
    accessor: 'expected_k_pct',
    disableFilters: true,
    sortType: basic,
    Cell: ({ value }) => {
      return format(value, value.toFixed(2))
    }
  },
  {
    Header: 'xBB/K',
    Footer: 'xBB/K',
    accessor: 'xbbk',
    disableFilters: true,
    sortType: basic,
    Cell: ({ value }) => {
      return format(value, value.toFixed(2))
    }
},
 {
    Header: 'xBB/Kpct',
    Footer: 'xBB/Kpct',
    accessor:'xbbk_rank',
    sortType: basic,
    disableFilters: true,
    Cell: ({ value }) => {
      return format(value, value.toFixed(3))
    }  
  },
  {
    Header: 'BW Points',
    Footer: 'BW Points',
    accessor: '3M Batting Pct',
    disableFilters: true,
    sortType: basic,
    Cell: ({ value }) => {
      return format(value, value.toFixed(1))
    }
},
 {
    Header: 'RK(seas)',
    Footer: 'RK(seas)',
    accessor: '3M Batting Rank',
    sortType: basic,
    disableFilters: true
  },
]
