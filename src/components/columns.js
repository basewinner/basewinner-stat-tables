import { format } from 'date-fns'
import { basic }from './sortTypes'

export const COLUMNS = [
  {
    Header: 'Name',
    Footer: 'Name',
    accessor: 'Name',
    disableFilters: true,
    
  },
  {
    Header: 'Team',
    Footer: 'Team',
    accessor: 'Team',
    width: '40',
  },

  {
    Header: 'PA',
    Footer: 'PA',
    accessor: 'PA',
    disableFilters: true,
  },
  {
    Header: 'HR',
    Footer: 'HR',
    accessor: 'HR',
    disableFilters: true,
  },
  {
    Header: 'K%',
    Footer: 'K%',
    accessor: 'K%',
    disableFilters: true,
    Cell: ({ value }) => {
      return format(value, value.toFixed(2))
    }
  },
  {
    Header: 'BB%',
    Footer: 'BB%',
    accessor: 'BB%',
    disableFilters: true,
    Cell: ({ value }) => {
      return format(value, value.toFixed(2))
    }
  },
  {
    Header: 'xwOBA',
    Footer: 'xwOBA',
    accessor: 'xwOBA',
    disableFilters: true,
    sortType: basic,
    Cell: ({ value }) => {
      return format(value, value.toFixed(3))
    }
  },
  {
    Header: 'wRC+',
    Footer: 'wRC+',
    accessor: 'wRC+',
    disableFilters: true,
    className: "right"
  },
]

