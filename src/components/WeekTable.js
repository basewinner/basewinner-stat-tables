import React, { useMemo, useEffect, useState } from 'react'
import { useTable, useFilters, usePagination , useSortBy } from 'react-table'
import { WEEK_COLUMNS } from './WeekColumns'
import './WeekTable.css'
import { ColumnFilter } from './ColumnFilter'
import axios from "axios";



export const WeekTable = () => {
  const columns = useMemo(() => WEEK_COLUMNS, [])
  const [data, setData] = useState([]);
 
  useEffect(() => {
    (async () => {
      const url = "https://www.basewinner.com/batting/aggregated_batting.json?cache=0"
      // const url = "aggregated_batting.json"
      const data = await axios(url);
      //This goes through weekly data the player name back into the weekly json
      let players = data.data.data.map(obj => ({
        ...obj,
        name: data.data.batters[obj.fgid],
        team: data.data.teams[obj.tid],
        key: obj.fgid + obj.tid + obj.week
      }));
      //Filtering out any player week data with less than 10 PA's
      let filteredPlayers = players.filter(p => p.pa >= 10);
      setData(filteredPlayers);
    })();
  }, []);


  const defaultColumn = React.useMemo(
    () => ({
      Filter: ColumnFilter
    }),
    []
  )

  const {
    getTableProps,
    getTableBodyProps,
    headerGroups,
    footerGroups,
    page,
    nextPage,
    previousPage,
    prepareRow,
    canNextPage,
    canPreviousPage,
    pageOptions,
    gotoPage,
    pageCount,
    setPageSize,
    state,
    allColumns,
    getToggleHideAllColumnsProps,
  
   
  } = useTable(
    {
      columns,
      data,
      defaultColumn,
      initialState: {pageSize: 20}
    },
    useFilters,
    useSortBy,
    usePagination
  )

  const { pageIndex, pageSize } = state

  

  return (
    <>
         {
         /* This will give you a checkkbox list to hide columns
          <div>
        <div>
          <Checkbox {...getToggleHideAllColumnsProps()} /> Toggle All
        </div>
        {allColumns.map(column => (
          <div key={column.id}>
            <label>
              <input type='checkbox' {...column.getToggleHiddenProps()} />{' '}
              {column.Header}
            </label>
          </div>
        ))}
        <br />
      </div> */}
      <table {...getTableProps()}>
        <thead>
          {headerGroups.map(headerGroup => (
            <tr {...headerGroup.getHeaderGroupProps()}>
              {headerGroup.headers.map(column => (
                <th {...column.getHeaderProps(column.getSortByToggleProps())}>
                  {column.render('Header')}
                  <span>
                    {column.isSorted
                      ? column.isSortedDesc
                        ? ' 🔽'
                        : ' 🔼'
                      : ''}
                  </span>
                  <div>{column.canFilter ? column.render('Filter') : null}</div>
                </th>
              ))}
            </tr>
          ))}
        </thead>
        <tbody {...getTableBodyProps()}>
          {page.map(row => {
            prepareRow(row)
            return (
              <tr {...row.getRowProps()}>
                {row.cells.map(cell => {
                  return <td {...cell.getCellProps()}>{cell.render('Cell')}</td>
                })}
              </tr>
            )
          })}
        </tbody>
        <tfoot>
          {footerGroups.map(footerGroup => (
            <tr {...footerGroup.getFooterGroupProps()}>
              {footerGroup.headers.map(column => (
                <td {...column.getFooterProps()}>{column.render('Footer')}</td>
              ))}
            </tr>
          ))}
        </tfoot>
      </table>
      <div>
        <span>
          Page{' '}
          <strong>
            {pageIndex +1} of {pageOptions.length}
          </strong>{' '}
        </span>
        <span>
          | Go to page:{' '}
          <input
            type='number'
            defaultValue={pageIndex + 1}
            onChange={e => {
              const pageNumber = e.target.value ? Number(e.target.value) - 1 : 0
              gotoPage(pageNumber)
            }}
            style={{ width: '50px' }}
          />
        </span>{' '}
        <select
          value={pageSize}
          onChange={e => setPageSize(Number(e.target.value))}>
          {[10, 20, 30, 50, 100, 200].map(pageSize => (
            <option key={pageSize} value={pageSize}>
              Page size: {pageSize}
            </option>
          ))}
        </select>
        <button onClick={() => gotoPage(0)} disabled={!canPreviousPage}>  {'<<'} </button>{' '}
        <button  onClick={() => previousPage()} disabled={!canPreviousPage}>Previous</button>
        <button  onClick={() => nextPage()} disabled={!canNextPage}>Next</button>
        <button onClick={() => gotoPage(pageCount -1)} disabled={!canNextPage}>
        {'>>'} 
        </button>
      </div>
    </>
  )
}